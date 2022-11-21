import pytest
from tap2shacl import TAP2SHACLConverter, TAP2APConverter, AP2SHACLConverter
from rdflib import Graph, URIRef
import pprint

tapFileName = "tests/TestData/booksTAP.csv"
configFileName = "tests/TestData/dctap.yml"
namespaceFileName = "tests/TestData/booksTAP-namespaces.csv"
aboutFileName = "tests/TestData/booksTAP-about.csv"
shapesFileName = "tests/TestData/booksTAP-shapes.csv"
shaclFileName = "tests/TestData/booksSHACL.ttl"


@pytest.fixture(scope="module")
def test_Converter():
    converter = TAP2SHACLConverter(tapFileName, configFileName)
    return converter


def test_init(test_Converter):
    c = test_Converter
    assert c.tap2apConverter
    assert c.tap
    assert len(c.tap["warnings_dict"]) == 2
    assert "shapes" in c.tap["shapes_dict"].keys()
    assert len(c.tap["shapes_dict"]["shapes"]) == 2
    assert c.ap == c.tap2apConverter.ap
    assert c.ap == c.ap2shaclConverter.ap
    assert c.sg != None


def test_convertTAP2AP(test_Converter):
    c = test_Converter
    assert len(c.ap.statementTemplates) == 0
    assert len(c.ap.metadata) == 0
    assert len(c.ap.namespaces) == 0
    assert len(c.ap.shapeInfo) == 0
    ap = c.convertTAP2AP(namespaceFileName, aboutFileName, shapesFileName)
    assert ap == c.ap
    assert len(ap.statementTemplates) == 7
    assert len(ap.metadata) == 6
    assert len(ap.namespaces) == 20
    assert len(ap.shapeInfo) == 2


def test_convertTAP2SHACL(test_Converter):
    c = test_Converter
    assert len(c.sg) == 0
    expected_sg = Graph().parse(shaclFileName)
    c.convertAP2SHACL()
    for stmt in expected_sg:
        assert stmt in c.sg
