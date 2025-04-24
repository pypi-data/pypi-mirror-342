import pandas as pd

import spacy
from spacy.pipeline import EntityRuler
from spacy.language import Language
from spacy.tokens import Span
from spacy_download import load_spacy
from cubicweb.utils import admincnx


EXCLUDED_SPACY_TYPE = ["MISC", "PER", "LOC", "ORG"]


def get_mapping(df):
    return list(zip(df.values[:, 0], df.values[:, 1]))


def create_instance_rules(appid, search_types):
    def instance_ruler(doc):
        with admincnx(appid) as cnx:
            spans = []
            for entity in doc:
                if (
                    entity.is_stop
                    or entity.is_punct
                    or entity.pos_ in ["VERB", "PRON", "SPACE"]
                ):
                    continue
                labels = []
                if entity.ent_type_:
                    labels.append(entity.ent_type_)
                for etype, attr_name in search_types:
                    res = cnx.execute(
                        f"Any X WHERE X is {etype}, X {attr_name} ILIKE '{entity.text}'"
                    )
                    for eid in res:
                        labels.append(f"{etype}:{attr_name}")
                if labels:
                    spans.append(
                        Span(doc, entity.i, entity.i + 1, label=", ".join(labels))
                    )
                else:
                    spans.append(Span(doc, entity.i, entity.i + 1, label="VALUE"))
            if spans:
                doc.set_ents(spans, default="unmodified")
        return doc

    return Language.component("instance_ruler", func=instance_ruler)


class DataExtractor:
    def __init__(self, mapping, instance_file=None, appid=None):
        self._make_mapping(mapping)
        self.nlp = load_spacy("fr_core_news_md")
        self.categorizer = spacy.blank("fr")
        Language.factory("ent_ruler", func=self.get_entity_ruler)
        self.nlp.add_pipe("ent_ruler", before="ner", name="etype")
        if appid and instance_file and instance_file.is_file():
            search_types = pd.read_csv(instance_file, delimiter=";").values.tolist()
            self._instance_ruler = create_instance_rules(appid, search_types)
            self.nlp.add_pipe("instance_ruler", last=True)
        self.nlp.disable_pipes("ner")

    def _make_mapping(self, mapping):
        self.mapping = []
        for label, pattern in mapping:
            self.mapping.append(
                {
                    "label": label,
                    "pattern": [
                        {"LOWER": {"FUZZY1": w.lower()}} for w in str(pattern).split()
                    ],
                }
            )

    def get_entity_ruler(self, nlp, name):
        ruler = EntityRuler(nlp)
        ruler.add_patterns(self.mapping)
        return ruler

    def extract_concept(self, content):
        doc = self.nlp(content)
        concepts = {}
        for ent in doc.ents:
            concepts.setdefault(ent.label_, []).append(ent.text)
        return concepts


def prepare_attr_concept(mapping):
    attr_concept = set()
    attr_nodes_for_name = {}
    for attr_node, trad in mapping:
        entity, attr = attr_node.split("#", 1)
        attr_concept.add((attr, trad))
        attr_nodes_for_name.setdefault(attr, []).append(attr_node)
    return list(attr_concept), attr_nodes_for_name


class EntityExtractor(DataExtractor):
    def __init__(self, entity_trans, attr_trans, instance_file=None, appid=None):
        self.entity_concept = get_mapping(entity_trans)
        self.attr_concept, self.attr_nodes_for_name = prepare_attr_concept(
            get_mapping(attr_trans)
        )
        super().__init__(self.entity_concept + self.attr_concept, instance_file, appid)
        self.entities = [etype for etype, _ in self.entity_concept]
        self.attributes = [etype for etype, _ in self.attr_concept]

    def get_nlp_analyze(self, content):
        return self.nlp(content)

    def detect_values(self, doc):
        values = []
        for token in doc:
            if token.is_stop:
                continue
            if token.pos_ in ["VERB", "PUNCT"]:
                continue
            for ent in doc.ents:
                if ent.label_ in EXCLUDED_SPACY_TYPE:
                    continue
                if token.text in ent.text:
                    break
            else:
                values.append(token.text)
        return values

    def associate_value_with_ent(self, doc, entity_ents, possible_values):
        association = {}
        df = pd.DataFrame()
        for pv in possible_values:
            for ne_i, ne in enumerate(doc.ents):
                for i in range(ne.start, ne.end):
                    df.loc[ne_i, ["D"]] = abs(ne.start - pv.i)
                    val = doc[i]
                    for child in val.children:
                        if child == pv:
                            association[pv] = ne
            if pv not in association:
                association[pv] = doc.ents[df.idxmin()["D"]]
        return {v: k for k, v in association.items()}

    def query_analyser(self, content):
        doc = self.get_nlp_analyze(content)
        entity_ents = [e.text for e in doc.ents if e.label_ != "VALUE"]
        possible_values = [
            t
            for t in doc
            if t.pos_ in ["NOUN", "PROPN", "NUM"] and t.text not in entity_ents
        ]
        values = self.associate_value_with_ent(doc, entity_ents, possible_values)
        analyse = {}
        for named_entity in doc.ents:
            cw_type = named_entity.label_
            cw_descr = {}
            if ":" in cw_type:
                etype, attr_name = cw_type.split(":")
                cw_descr["type"] = "instance"
                cw_descr["instance_type"] = etype
                cw_descr["instance_attr_name"] = attr_name
                cw_descr["expected_value"] = str(named_entity)
            elif cw_type in self.entities:
                cw_descr["type"] = "entity"
                if named_entity in values:
                    cw_descr["expected_value"] = values[named_entity].text
            elif cw_type in self.attributes:
                cw_descr["type"] = "attribute"
                if named_entity in values:
                    cw_descr["expected_value"] = values[named_entity].text
            if cw_descr:
                analyse.setdefault(cw_type, []).append(cw_descr)
        return analyse
