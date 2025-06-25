import pytest
from dctap import csvreader  # , TAPShape, TAPStatementConstraint
from dctap.config import get_config
from ap import AP, StatementTemplate, ShapeInfo
from tap2ap import TAP2APConverter

tapFileName = "tests/tap2ap/TestData/tap.csv"
configFileName = "dctap.yml"
namespaceFileName = "tests/tap2ap/TestData/namespaces.csv"
aboutFileName = "tests/tap2ap/TestData/about.csv"
shapesFileName = "tests/tap2ap/TestData/shapes.csv"


@pytest.fixture(scope="module")
def test_Converter():
    Converter = TAP2APConverter(tapFileName, configFileName)
    return Converter


def test_initConverter(test_Converter):
    c = test_Converter
    assert c
    assert len(c.tap["warnings_dict"]) == 2
    assert "shapes" in c.tap["shapes_dict"].keys()
    shapes_list = c.tap["shapes_dict"]["shapes"]
    assert len(shapes_list) == 2


def test_convert_namespaces(test_Converter):
    c = test_Converter
    assert c.ap.namespaces == {}
    # first read in from TAP yaml file
    c.convert_namespaces("TAP")
    assert len(c.ap.namespaces) == 15
    assert c.ap.namespaces["xsd"] == "http://www.w3.org/2001/XMLSchema#"
    assert c.ap.namespaces["ex"] == "http://example.org/"
    # then overwrite/append from namespaces csv file
    c.convert_namespaces("csv", namespaceFileName)
    assert len(c.ap.namespaces) == 19
    # sh is declared without colon
    assert c.ap.namespaces["sh"] == "http://www.w3.org/ns/shacl#"
    # rdf: is declared with colon
    assert c.ap.namespaces["rdf"] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    # ex is changed
    assert c.ap.namespaces["ex"] == "http://example.org/terms#"
    # default has no prefix declared
    print(c.ap.namespaces)
    assert c.ap.namespaces["default"] == "http://example.org/terms#"


def test_load_AP_metadata(test_Converter):
    c = test_Converter
    assert c.ap.metadata == {}
    c.load_AP_Metadata(aboutFileName)
    assert (
        c.ap.metadata["url"]
        == "https://docs.google.com/spreadsheets/d/1Vr_x1ckpxG0v8oq7FGB2Qea8G3ESPFvUWK89H0wJH9w/edit#gid=424305041"
    )
    assert c.ap.metadata["title"] == "Simple book AP"
    assert c.ap.metadata["description"] == "Simple DC TAP for books"
    assert c.ap.metadata["author"] == "Phil Barker"
    assert c.ap.metadata["date"] == "2022-01-14"
    assert c.ap.metadata["lang"] == "en"


def test_load_shapeInfo(test_Converter):
    # this tests a method from the imported AP classes
    c = test_Converter
    assert c.ap.shapeInfo == {}
    c.ap.load_shapeInfo(shapesFileName)
    assert len(c.ap.shapeInfo) == 2
    book_shapeInfo = c.ap.shapeInfo["BookShape"]
    author_shapeInfo = c.ap.shapeInfo["AuthorShape"]
    assert book_shapeInfo.label == {"en": "Book"}
    assert author_shapeInfo.label == {"en": "Author"}
    assert author_shapeInfo.targets == {
        "objectsof": ["dct:creator"],
        "class": ["sdo:Person"],
    }
    assert author_shapeInfo.closed == True
    assert author_shapeInfo.ignoreProps == ["rdf:type"]
    assert author_shapeInfo.mandatory == False
    assert author_shapeInfo.severity == "warning"


def test_check_shapeID(test_Converter):
    c = test_Converter
    sh_id = "AuthorShape"
    sh_id = c.check_shapeID(sh_id)
    assert sh_id == "AuthorShape"
    sh_id = 2
    with pytest.raises(TypeError) as e:
        sh_id = c.check_shapeID(sh_id)
    assert str(e.value) == "shapeID must be a string."
    sh_id = "notAShapeID"
    with pytest.raises(ValueError) as e:
        sh_id = c.check_shapeID(sh_id)
    assert str(e.value) == "No shape info for notAShapeID"


def test_convert_propertyIDs(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    p_id = "test1, test2 test3,test4;test5\ntest6"
    c.convert_propertyIDs(p_id, ps)
    for p in ["test1", "test2", "test3", "test4", "test5", "test6"]:
        assert p in ps.properties
    p_id = ["test1"]
    with pytest.raises(TypeError) as e:
        c.convert_propertyIDs(p_id, ps)
    assert str(e.value) == "Properties must be passed in a string."


def test_convert_labels(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    label = "test one"
    c.convert_labels(label, ps)
    ps.labels == [{"en": "test one"}]
    label = ["test one"]
    with pytest.raises(TypeError) as e:
        c.convert_labels(label, ps)
    assert str(e.value) == "Labels must be passed in a string."


def test_convert_mandatory(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    m = "False"
    c.convert_mandatory(m, ps)
    assert ps.mandatory == False
    m = "True"
    c.convert_mandatory(m, ps)
    assert ps.mandatory == True
    m = "No"
    c.convert_mandatory(m, ps)
    assert ps.mandatory == False
    m = True
    with pytest.raises(TypeError) as e:
        c.convert_mandatory(m, ps)
    assert str(e.value) == "Value for mandatory must be a string."
    m = "Allowed"
    with pytest.raises(ValueError) as e:
        c.convert_mandatory(m, ps)
    assert str(e.value) == "Value for mandatory not recognised: Allowed"


def test_convert_repeatable(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    r = "False"
    c.convert_repeatable(r, ps)
    assert ps.repeatable == False
    r = "True"
    c.convert_repeatable(r, ps)
    assert ps.repeatable == True
    r = "No"
    c.convert_repeatable(r, ps)
    assert ps.repeatable == False
    r = True
    with pytest.raises(TypeError) as e:
        c.convert_repeatable(r, ps)
    assert str(e.value) == "Value for repeatable must be a string."
    r = "Allowed"
    with pytest.raises(ValueError) as e:
        c.convert_repeatable(r, ps)
    assert str(e.value) == "Value for repeatable not recognised: Allowed"


def test_convert_valueNodeTypes(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    vNT = "IRI, bnode"
    c.convert_valueNodeTypes(vNT, ps)
    assert "IRI" in ps.valueNodeTypes
    assert "bnode" in ps.valueNodeTypes
    vNT = ["IRI", "bnode"]
    with pytest.raises(TypeError) as e:
        c.convert_valueNodeTypes(vNT, ps)
    assert str(e.value) == "Value for node types must be a string."


def test_convert_valueDataTypes(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    vDT = "xsd:date; xsd:time"
    c.convert_valueDataTypes(vDT, ps)
    assert "xsd:date" in ps.valueDataTypes
    assert "xsd:time" in ps.valueDataTypes
    vDT = ["xsd:date", "xsd:time"]
    with pytest.raises(TypeError) as e:
        c.convert_valueDataTypes(vDT, ps)
    assert str(e.value) == "Value for data types must be a string."


def test_convert_valueConstraints(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    vC = """orgType:AssessmentBody
orgType:Business"""
    c.convert_valueConstraints(vC, ps)
    assert "orgType:AssessmentBody" in ps.valueConstraints
    assert "orgType:Business" in ps.valueConstraints
    vC = ["orgType:Government", "orgType:HEI"]
    c.convert_valueConstraints(vC, ps)
    assert "orgType:Government" in ps.valueConstraints
    assert "orgType:HEI" in ps.valueConstraints
    vC = 2
    c.convert_valueConstraints(vC, ps)
    assert "2" in ps.valueConstraints
    #    vC = [3, 4]
    #    c.convert_valueConstraints(vC, ps)
    #    assert "3" in ps.valueConstraints
    #    assert "4" in ps.valueConstraints
    vC = 2.0
    with pytest.raises(TypeError) as e:
        c.convert_valueConstraints(vC, ps)
    assert str(e.value) == "Value for constraints must be a string, integer or a list."
    vC = [2.0]
    with pytest.raises(TypeError) as e:
        c.convert_valueConstraints(vC, ps)
    assert str(e.value) == "Value for constraint must be a string or integer."
    vC = "\."  # testing how escape chars are handled
    c.convert_valueConstraints(vC, ps)
    print(ps.valueConstraints)  # stored as \\.
    assert "\." in ps.valueConstraints  # passes
    assert "\\." in ps.valueConstraints  # also passes


def test_convert_valueConstraintType(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    vCT = "pattern"
    c.convert_valueConstraintType(vCT, ps)
    assert ps.valueConstraintType == "pattern"
    vCT = None
    with pytest.raises(TypeError) as e:
        c.convert_valueConstraintType(vCT, ps)
    assert str(e.value) == "Value for constraint type must be a string."


def test_convert_shapes(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    shapes = "AddressShape,ContactShape"
    addressShapeInfo = ShapeInfo(label="Address")
    contactShapeInfo = ShapeInfo(label="Contact")
    c.ap.add_shapeInfo("AddressShape", addressShapeInfo)
    c.ap.add_shapeInfo("ContactShape", contactShapeInfo)
    c.convert_valueShapes(shapes, ps)
    for sh in ["AddressShape", "ContactShape"]:
        assert sh in ps.valueShapes
    shapes = ["AddressShape", "ContactShape"]
    with pytest.raises(TypeError) as e:
        c.convert_valueShapes(shapes, ps)
    assert str(e.value) == "Value for shapes must be a string."
    shapes = "notAShapeID"
    with pytest.raises(ValueError) as e:
        c.convert_valueShapes(shapes, ps)
    assert str(e.value) == "No shape info for notAShapeID"


def test_convert_notes(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    note = "test one"
    c.convert_notes(note, ps)
    assert ps.notes == {"en": "test one"}
    note = 42
    with pytest.raises(TypeError) as e:
        c.convert_notes(note, ps)
    assert str(e.value) == "Notes must be passed in a string."


def test_convert_propertyDescriptions(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    descr = "test one"
    c.convert_propertyDescriptions(descr, ps)
    assert ps.propertyDescriptions == {"en": "test one"}
    descr = 42
    with pytest.raises(TypeError) as e:
        c.convert_propertyDescriptions(descr, ps)
    assert str(e.value) == "Property descriptions must be passed in a string."


def test_convert_severity(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    sev = "Violation"
    c.convert_severity(sev, ps)
    assert ps.severity == "Violation"
    sev = None
    with pytest.raises(TypeError) as e:
        c.convert_severity(sev, ps)
    assert str(e.value) == "Value for severity must be a string."

def test_convert_messages(test_Converter):
    c = test_Converter
    ps = StatementTemplate()
    message = "test one"
    c.convert_messages(message, ps)
    assert ps.messages == {"en": "test one"}
    message = 42
    with pytest.raises(TypeError) as e:
        c.convert_messages(message, ps)
    assert str(e.value) == "Messages must be passed in a string."

def test_convert_TAP_AP(test_Converter):
    c = test_Converter
    c.convert_TAP_AP()
