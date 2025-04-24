from unittest import TestCase

import tempfile
from pathlib import Path

from rql import parse

from utils import generate_schema_data
from cubicweb_spacyquery.query_extractor import QueryExtractor

import pandas as pd


with tempfile.TemporaryDirectory() as tmpdirname:
    _, _, rfile = generate_schema_data(Path(tmpdirname))
    relations = pd.read_csv(rfile, sep=";")
    QE = QueryExtractor(relations)


class QueryExtractorTC(TestCase):
    def assertRQLEquivalent(self, query1: str, query2: str):
        rql1 = parse(query1)
        rql2 = parse(query2)
        self.assertTrue(rql1.is_equivalent(rql2))

    def assertRQLEquivalentInList(self, query: str, queries: list[str]):
        for test_query in queries:
            try:
                self.assertRQLEquivalent(query, test_query)
            except AssertionError:
                pass
            else:
                break
        else:
            queries_str = "\n" + "\n".join(queries)
            self.fail(f"{query} not found in {queries_str}")

    def test_only_one_etype(self):
        queries = QE.get_queries(["Person"], [])
        expected = "Any PERSON WHERE PERSON is Person"
        self.assertRQLEquivalentInList(expected, [q.to_rql() for q in queries])

    def test_simple_entity_link(self):
        queries = QE.get_queries(["Person", "Organization"], [])
        expected = (
            "Any ORGANIZATION, PERSON WHERE ORGANIZATION is Organization,"
            " PERSON is Person, PERSON works_for ORGANIZATION"
        )
        self.assertRQLEquivalentInList(expected, [q.to_rql() for q in queries])

    def test_simple_entity_link_and_attr(self):
        queries = QE.get_queries(
            ["Person", "Organization"], ["Person#firstname", "Organization#name"]
        )
        expected = (
            "Any "
            "ORGANIZATION,"
            "ORGANIZATION_NAME, "
            "PERSON, "
            "PERSON_FIRSTNAME "
            "WHERE "
            "ORGANIZATION name ORGANIZATION_NAME,"
            "PERSON firstname PERSON_FIRSTNAME,"
            "ORGANIZATION is Organization, "
            "PERSON is Person,"
            "PERSON works_for ORGANIZATION"
        )
        self.assertRQLEquivalentInList(expected, [q.to_rql() for q in queries])

    def test_simple_entity_link_and_multi_attr(self):
        queries = QE.get_queries(
            ["Person", "Organization"],
            ["Person#firstname", "Person#lastname", "Organization#name"],
        )
        expected = (
            "Any "
            "ORGANIZATION, "
            "ORGANIZATION_NAME, "
            "PERSON, "
            "PERSON_FIRSTNAME, "
            "PERSON_LASTNAME "
            "WHERE "
            "ORGANIZATION name ORGANIZATION_NAME, "
            "PERSON firstname PERSON_FIRSTNAME, "
            "PERSON lastname PERSON_LASTNAME, "
            "ORGANIZATION is Organization, "
            "PERSON is Person,"
            "PERSON works_for ORGANIZATION"
        )
        self.assertRQLEquivalentInList(expected, [q.to_rql() for q in queries])

    def test_missing_entity_link_and_attr(self):
        queries = QE.get_queries(
            ["Person"],
            ["Person#firstname", "Organization#name"],
        )
        expected = (
            "Any "
            "ORGANIZATION, "
            "ORGANIZATION_NAME, "
            "PERSON, "
            "PERSON_FIRSTNAME "
            "WHERE "
            "ORGANIZATION name ORGANIZATION_NAME, "
            "PERSON firstname PERSON_FIRSTNAME, "
            "ORGANIZATION is Organization, "
            "PERSON is Person, "
            "PERSON works_for ORGANIZATION"
        )
        self.assertRQLEquivalentInList(expected, [q.to_rql() for q in queries])

    def test_first(self):
        queries = QE.get_queries(["Person", "SubComponent"], [])
        expected = (
            "Any "
            "COMPONENT, "
            "PERSON, "
            "PROJECT, "
            "SUBCOMPONENT "
            "WHERE "
            "COMPONENT is Component, "
            "PERSON is Person, "
            "PROJECT is Project, "
            "SUBCOMPONENT is SubComponent, "
            "COMPONENT has_subcomponent SUBCOMPONENT, "
            "PROJECT includes COMPONENT, "
            "PROJECT involves PERSON"
        )
        self.assertRQLEquivalentInList(expected, [q.to_rql() for q in queries])

    def test_second(self):
        queries = QE.get_queries(["Person", "Theme"], [])
        expected = (
            "Any "
            "DOCUMENT, "
            "PERSON,  "
            "THEME "
            "WHERE"
            "DOCUMENT is Document, "
            "PERSON is Person, "
            "THEME is Theme, "
            "DOCUMENT relates_to THEME, "
            "PERSON writes DOCUMENT"
        )
        self.assertRQLEquivalentInList(expected, [q.to_rql() for q in queries])

    def test_simple_entity_link_and_attr_value(self):
        queries = QE.get_queries(
            ["Person", "Organization"],
            ["Person#firstname", "Organization#name#Lglb"],
        )
        expected = (
            "Any "
            "ORGANIZATION, "
            "PERSON, "
            "PERSON_FIRSTNAME "
            "WHERE "
            "ORGANIZATION name 'Lglb', "
            "PERSON firstname PERSON_FIRSTNAME, "
            "ORGANIZATION is Organization, "
            "PERSON is Person, "
            "PERSON works_for ORGANIZATION"
        )
        self.assertRQLEquivalentInList(expected, [q.to_rql() for q in queries])

    def test_simple_entity_link_and_attr_value_ilike(self):
        queries = QE.get_queries(
            ["Person", "Organization"],
            ["Person#firstname", "Organization#name#lglb#I"],
        )
        expected = (
            "Any "
            "ORGANIZATION, "
            "PERSON, "
            "PERSON_FIRSTNAME "
            "WHERE "
            "ORGANIZATION name ILIKE 'lglb', "
            "PERSON firstname PERSON_FIRSTNAME, "
            "ORGANIZATION is Organization, "
            "PERSON is Person,"
            "PERSON works_for ORGANIZATION"
        )
        self.assertRQLEquivalentInList(expected, [q.to_rql() for q in queries])

    def test_simple_entity_link_and_attr_value_ilike2(self):
        queries = QE.get_queries(
            ["Person"],
            ["Person#firstname", "Organization#name#lglb#I"],
        )
        expected = (
            "Any "
            "ORGANIZATION, "
            "PERSON, "
            "PERSON_FIRSTNAME "
            "WHERE "
            "ORGANIZATION name ILIKE 'lglb', "
            "PERSON firstname PERSON_FIRSTNAME, "
            "ORGANIZATION is Organization,"
            "PERSON is Person, "
            "PERSON works_for ORGANIZATION"
        )
        self.assertRQLEquivalentInList(expected, [q.to_rql() for q in queries])

    def test_multi_values(self):
        queries = QE.get_queries(
            ["Project"],
            [
                "Organization#sector#énergie",
                "Component#type#centrale",
                "Component#version#1.2",
                "Project#name",
            ],
        )
        expected = (
            "Any "
            "COMPONENT, "
            "ORGANIZATION, "
            "PROJECT, "
            "PROJECT_NAME "
            "WHERE "
            "COMPONENT type 'centrale', "
            "COMPONENT version '1.2', "
            "ORGANIZATION sector 'énergie', "
            "PROJECT name PROJECT_NAME, "
            "COMPONENT is Component, "
            "ORGANIZATION is Organization, "
            "PROJECT is Project, "
            "PROJECT includes COMPONENT, "
            "PROJECT managed_by ORGANIZATION "
        )
        self.assertRQLEquivalentInList(expected, [q.to_rql() for q in queries])
