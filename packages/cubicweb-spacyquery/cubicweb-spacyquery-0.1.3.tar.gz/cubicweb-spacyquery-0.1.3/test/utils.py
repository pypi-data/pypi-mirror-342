import pandas as pd

entities = [
    ("Person", "Personne"),
    ("Organization", "Organisation"),
    ("Document", "Document"),
    ("Theme", "Thème"),
    ("Component", "Composant"),
    ("Project", "Projet"),
    ("SubComponent", "Sous-composant"),
]
entities_df = pd.DataFrame(entities, columns=["Entity", "Trad"])

attributes = [
    ("Person#firstname", "prénom"),
    ("Person#lastname", "nom"),
    ("Person#email", "courriel"),
    ("Organization#name", "nom"),
    ("Organization#sector", "secteur"),
    ("Document#title", "titre"),
    ("Document#creationDate", "date de création"),
    ("Theme#label", "libellé"),
    ("Component#version", "version"),
    ("Component#type", "type"),
    ("SubComponent#version", "version"),
    ("SubComponent#type", "type"),
    ("SubComponent#reference", "réference"),
    ("Project#name", "nom"),
    ("Project#startDate", "date de début"),
    ("Project#endDate", "date de fin"),
]
attributes_df = pd.DataFrame(attributes, columns=["Attribute", "Trad"])

relations = [
    # Attributes
    ("Person", "attribute", "Person#firstname"),
    ("Person", "attribute", "Person#lastname"),
    ("Person", "attribute", "Person#email"),
    ("Organization", "attribute", "Organization#name"),
    ("Organization", "attribute", "Organization#sector"),
    ("Document", "attribute", "Document#title"),
    ("Document", "attribute", "Document#creationDate"),
    ("Theme", "attribute", "Theme#label"),
    ("Component", "attribute", "Component#version"),
    ("Component", "attribute", "Component#type"),
    ("Project", "attribute", "Project#name"),
    ("Project", "attribute", "Project#startDate"),
    ("Project", "attribute", "Project#endDate"),
    # Entity-to-entity relations
    ("Person", "works_for", "Organization"),
    ("Person", "writes", "Document"),
    ("Document", "relates_to", "Theme"),
    ("Project", "involves", "Person"),
    ("Project", "includes", "Component"),
    ("Project", "managed_by", "Organization"),
    ("Component", "depends_on", "Component"),
    ("Component", "documents", "Document"),
    ("Component", "has_subcomponent", "SubComponent"),
]
relations_df = pd.DataFrame(relations, columns=["fe", "rel", "te"])


def generate_schema_data(directory):
    entity_file = directory / "entities.csv"
    attr_file = directory / "attributes.csv"
    relation_file = directory / "relations.csv"
    entities_df.to_csv(entity_file, index=False)
    attributes_df.to_csv(attr_file, index=False)
    relations_df.to_csv(relation_file, index=False, sep=";")
    return entity_file, attr_file, relation_file
