import polib

from pathlib import Path
from functools import cache

import pandas as pd

from cubicweb_spacyquery.spacy_extractor import (
    EntityExtractor,
)

from cubicweb_spacyquery.query_extractor import (
    QueryExtractor,
)


CW_EXCLUDED_ATTRS = ["creation_date", "modification_date", "cwuri"]
CUBES_ETYPES_RQL = "Any CE WHERE CE is CWEType, CE final False"


def from_relation_for_cwetype(cnx, cwetype):
    resp = cnx.execute(
        "Any RTN, TEN, GROUP_CONCAT(SUB_CLASSES_NAME) "
        " GROUPBY RTN, TEN "
        " WHERE X is CWRelation, X from_entity E, "
        " X relation_type RT, RT name RTN,"
        " X to_entity TE, TE name TEN,"
        " E name %(cwetype)s, "
        " SUB_CLASSES? specializes TE, "
        " SUB_CLASSES name SUB_CLASSES_NAME",
        {"cwetype": cwetype},
    )
    for relation, obj, sub_classes_names in resp:
        yield relation, obj
        if sub_classes_names:
            for sub_classes_name in sub_classes_names.split(","):
                yield relation, sub_classes_name


def attribute_for_etype(cnx, etype):
    res = cnx.execute(
        "Any CWAN WHERE CWA is CWAttribute, CWA relation_type CWAT,"
        " CWAT name CWAN, CWA from_entity E, E name '{:s}'".format(etype)
    )
    return [attr for attr, in res if attr not in CW_EXCLUDED_ATTRS]


def get_triples(cnx):
    triples = []
    for etype in cnx.execute(CUBES_ETYPES_RQL).entities():
        for rel, to_etype in from_relation_for_cwetype(cnx, etype.name):
            triples.append((etype.name, rel, to_etype))
        for attr_name in attribute_for_etype(cnx, etype.name):
            triples.append((etype.name, "attribute", f"{etype.name}#{attr_name}"))
    return triples


def get_triples_df(cnx):
    return pd.DataFrame(get_triples(cnx), columns=["fe", "rel", "te"])


def to_file(cnx, filename):
    df = get_triples(cnx)
    df.to_csv(filename, sep=";", index=False)


def entities_name(cnx, filename, translation):
    df = entities_name_df(cnx, translation)
    df.to_csv(filename, sep=",", index=False)


def entities_name_df(cnx, translation):
    entities_name = []
    for etype in cnx.execute(CUBES_ETYPES_RQL).entities():
        entities_name.append(
            (etype.name, f"{translation.get(etype.name) or etype.name}")
        )
    return pd.DataFrame(entities_name, columns=["Entity", "Translation"])


def attributes_name_df(cnx, translation):
    df = pd.DataFrame(columns=["Attribute", "Translation"])
    for i, etype in enumerate(cnx.execute(CUBES_ETYPES_RQL).entities()):
        for attr in attribute_for_etype(cnx, etype.name):
            df.loc[i] = (f"{etype.name}#{attr}", f"{translation.get(attr) or attr}")
    return df


def attributes_name(cnx, filename, translation):
    df = attributes_name_df(cnx, translation)
    df.to_csv(filename, sep=",", index=False)


def mo_to_translation(mo_file_path):
    mo = polib.mofile(mo_file_path)
    translations = {}
    for entry in mo:
        translations[entry.msgid] = entry.msgstr
    return {entry.msgid: entry.msgstr for entry in mo if entry.msgstr != ""}


def prepare(cnx, appid):
    instance_home = Path(cnx.repo.config.instance_home(appid))
    translation = mo_to_translation(
        instance_home / "i18n" / "fr" / "LC_MESSAGES" / "cubicweb.mo"
    )
    to_file(cnx, instance_home / "spacy_etype.csv")
    entities_name(cnx, instance_home / "spacy_entities.csv", translation)
    attributes_name(cnx, instance_home / "spacy_attributes.csv", translation)


@cache
def get_query_extractor(cnx):
    appid = cnx.repo.config.appid
    instance_home = Path(cnx.repo.config.instance_home(appid))
    spacy_etype_path = instance_home / "spacy_etype.csv"
    if spacy_etype_path.is_file():
        triples_df = pd.read_csv(spacy_etype_path, sep=";")
    else:
        triples_df = get_triples_df(cnx)

    return QueryExtractor(triples_df, instance_home / "spacy_weight.csv")


@cache
def get_entity_extractor(cnx):
    if not hasattr(cnx, "repo"):
        cnx = cnx.cnx
    appid = cnx.repo.config.appid
    instance_home = Path(cnx.repo.config.instance_home(appid))
    translation = mo_to_translation(
        instance_home / "i18n" / "fr" / "LC_MESSAGES" / "cubicweb.mo"
    )
    spacy_entities_path = instance_home / "spacy_entities.csv"
    if spacy_entities_path.is_file():
        spacy_entities = pd.read_csv(spacy_entities_path, sep=",")
    else:
        spacy_entities = entities_name_df(cnx, translation)
    spacy_attributes_path = instance_home / "spacy_attributes.csv"
    if spacy_attributes_path.is_file():
        spacy_attributes = pd.read_csv(spacy_attributes_path, sep=",")
    else:
        spacy_attributes = attributes_name_df(cnx, translation)
    return EntityExtractor(
        spacy_entities,
        spacy_attributes,
        instance_home / "spacy_instances.csv",
        appid,
    )


def ask(cnx, question):
    qe = get_query_extractor(cnx)
    ee = get_entity_extractor(cnx)

    qa = ee.query_analyser(question)
    nodes, attr_nodes, attr_names = [], [], []

    for key, data in qa.items():
        for elm in data:
            if elm["type"] == "entity":
                nodes.append(key)
            elif elm["type"] == "instance":
                etype = elm["instance_type"]
                attr_name = elm["instance_attr_name"]
                expected_value = elm["expected_value"]
                attr_nodes.append(f"{etype}#{attr_name}#{expected_value}#I")
            elif elm["type"] == "attribute":
                attr_names.append(key)
    extra_attr = []
    for name in attr_names:
        entity_found = False
        for entity in nodes:
            if f"{entity}#{name}" in ee.attr_nodes_for_name[name]:
                attr_nodes.append(f"{entity}#{name}")
                entity_found = True
        if not entity_found:
            extra_attr.extend(ee.attr_nodes_for_name[name])

    if extra_attr:
        queries = []
        for ex_attr in extra_attr:
            attr_nodes_b = attr_nodes[:]
            attr_nodes_b.append(ex_attr)
            sub_query = qe.get_queries(nodes, attr_nodes_b)
            queries.append(sub_query)
        return queries
    return qe.get_queries(nodes, attr_nodes)
