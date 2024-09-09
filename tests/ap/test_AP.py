import pytest
from ap import AP, StatementTemplate, ShapeInfo

namespace_fname = "tests/ap/TestData/namespaces.csv"
metadata_fname = "tests/ap/TestData/about.csv"
shapeInfo_fname = "tests/ap/TestData/shapes.csv"


@pytest.fixture(scope="module")
def test_AP():
    ap = AP()
    return ap


@pytest.fixture(scope="module")
def test_StatementTemplate():
    ps = StatementTemplate()
    return ps


def test_init_defaults(test_AP):
    assert test_AP
    assert test_AP.metadata == {}
    assert test_AP.namespaces == {}
    assert test_AP.shapeInfo == {}
    assert test_AP.statementTemplates == []


def test_add_namespace(test_AP):
    ap = test_AP
    ap.add_namespace("dct", "http://purl.org/dc/terms/")
    ap.add_namespace("rdf:", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    assert ap.namespaces["dct"] == "http://purl.org/dc/terms/"
    assert ap.namespaces["rdf"] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    ap.add_namespace("", "http://example.org/")
    assert ap.namespaces["default"] == "http://example.org/"
    ap.add_namespace(":", "http://example.org/colon#")
    assert ap.namespaces["default"] == "http://example.org/colon#"
    ap.add_namespace("ex:", "http://example.org/colon#")
    assert ap.namespaces["ex"] == "http://example.org/colon#"
    with pytest.raises(TypeError):
        ap.add_namespace(27, "http://purl.org/dc/terms/")
    with pytest.raises(TypeError) as e:
        ap.add_namespace("dct", ["http://purl.org/dc/terms/"])
    assert str(e.value) == "Both ns and URI must be strings."


def test_load_namespaces(test_AP):
    ap = test_AP
    ap.load_namespaces(namespace_fname)
    assert ap.namespaces["foaf"] == "http://xmlns.com/foaf/0.1/"
    assert ap.namespaces["base"] == "http://example.org/"


def test_add_metadata(test_AP):
    ap = test_AP
    ap.add_metadata("dct:title", "this is the title")
    ap.add_metadata("dct:date", "2021-07-01")
    assert ap.metadata["dct:title"] == "this is the title"
    assert ap.metadata["dct:date"] == "2021-07-01"
    with pytest.raises(TypeError) as e:
        ap.add_namespace("dct:title", 22)
    assert str(e.value) == "Both ns and URI must be strings."


def test_load_metadata(test_AP):
    ap = test_AP
    ap.load_metadata(metadata_fname)
    assert (
        ap.metadata["url"]
        == "https://docs.google.com/spreadsheets/d/1Vr_x1ckpxG0v8oq7FGB2Qea8G3ESPFvUWK89H0wJH9w/edit#gid=424305041"
    )
    assert ap.metadata["title"] == "Simple book AP"
    assert ap.metadata["description"] == "Simple DC TAP for books"
    assert ap.metadata["author"] == "Phil Barker"
    assert ap.metadata["date"] == "2022-01-14"
    assert ap.metadata["lang"] == "en"


def test_add_shapeInfo(test_AP):
    ap = test_AP
    shapeInfo = ShapeInfo()
    shapeInfo.id = "testShape"
    shapeInfo.label = "test shape"
    shapeInfo.comment = "just a shape for tests"
    shapeInfo.target = {"objectsof": ["dc:author"]}
    shapeInfo.closed = True
    shapeInfo.mandatory = False
    shapeInfo.severity = "Warning"
    shapeInfo.ignoreProps = ["p1", "p2"]
    ap.add_shapeInfo("testShape", shapeInfo)
    assert ap.shapeInfo["testShape"].label == "test shape"
    assert ap.shapeInfo["testShape"].closed == True
    with pytest.raises(TypeError) as e:
        ap.add_shapeInfo("testShape", "just the label")
    assert str(e.value) == "Info must be of ShapeInfo type, id must be a string."
    assert ap.shapeInfo["testShape"].ignoreProps == ["p1", "p2"]


def test_load_shapeInfo(test_AP):
    ap = test_AP
    ap.load_shapeInfo(shapeInfo_fname)
    assert len(ap.shapeInfo) == 3
    assert "testShape" in ap.shapeInfo.keys()
    assert "BookShape" in ap.shapeInfo.keys()
    assert "AuthorShape" in ap.shapeInfo.keys()
    assert ap.shapeInfo["AuthorShape"] == ShapeInfo(
        id="AuthorShape",
        label={"en": "Author"},
        comment={"en": "Shape for describing authors"},
        targets={"objectsof": ["dct:creator"], "class": ["sdo:Person"]},
        closed=True,
        ignoreProps=["rdf:type"],
        mandatory=False,
        severity="warning",
        note={},
    )
