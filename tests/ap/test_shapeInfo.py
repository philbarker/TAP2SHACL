import pytest
from ap import ShapeInfo, read_shapeInfoDict
from ap.shapeInfo import ShapeInfo


@pytest.fixture(scope="module")
def test_ShapeInfo():
    sh = ShapeInfo()
    return sh


def test_initShapeInfo(test_ShapeInfo: ShapeInfo):
    sh = test_ShapeInfo
    assert sh.id == ""
    assert sh.label == {}  # lang map of "lang": "value" pairs
    assert sh.comment == {}  # lang map
    assert sh.targets == {}  # "type" : "target" pairs, type maps to SHACL
    # FIXME: should allow list of targets for each type.
    assert sh.closed == False  # boolean, True = closed, False = open
    assert sh.ignoreProps == []  # list of propety ids
    assert sh.mandatory == False  # boolean, True = mandatory, False = optional
    assert sh.severity == ""  # string should map to SHACL vals or similar
    assert sh.note == {}  # lang map


def test_set_id(test_ShapeInfo: ShapeInfo):
    sh = test_ShapeInfo
    assert sh.id == ""
    sh.set_id("TestShape")
    assert sh.id == "TestShape"
    with pytest.raises(TypeError) as e:
        sh.set_id(1)
    assert str(e.value) == "Shape identifier must be a string."
    assert sh.id == "TestShape"


def test_add_label(test_ShapeInfo: ShapeInfo):
    sh = test_ShapeInfo
    assert sh.label == {}
    sh.add_label("en", "Test")
    assert sh.label == {"en": "Test"}
    sh.add_label("es", "Prueba")
    assert sh.label == {"en": "Test", "es": "Prueba"}
    with pytest.raises(TypeError) as e:
        sh.add_label("en", 2)
    assert str(e.value) == "Language identifier and label must be strings."
    assert sh.label == {"en": "Test", "es": "Prueba"}
    sh.add_label("en", "Probe")
    assert sh.label == {"en": "Probe", "es": "Prueba"}


def test_append_target(test_ShapeInfo: ShapeInfo):
    sh = test_ShapeInfo
    assert sh.targets == {}
    sh.append_target("dc:author", "objectsOf")
    assert sh.targets == {"objectsof": ["dc:author"]}
    sh.append_target("dc:Agent", "Class")
    assert sh.targets == {"objectsof": ["dc:author"], "class": ["dc:Agent"]}
    with pytest.raises(TypeError) as e:
        sh.append_target("instance", 2)
    assert str(e.value) == "Target and type must be strings."
    sh.append_target("dc:creator", "objectsOf")
    # adding second target to objectsof
    assert sh.targets == {
        "objectsof": ["dc:author", "dc:creator"],
        "class": ["dc:Agent"],
    }
    # add two targets in one string
    sh.append_target("dc:creator, dc:contributor", "subjectsOf")
    assert sh.targets == {
        "objectsof": ["dc:author", "dc:creator"],
        "class": ["dc:Agent"],
        "subjectsof": ["dc:creator", "dc:contributor"],
    }


def test_set_closed(test_ShapeInfo: ShapeInfo):
    sh = test_ShapeInfo
    assert sh.closed == False
    sh.set_closed(True)
    assert sh.closed == True
    sh.set_closed(False)
    assert sh.closed == False
    sh.set_closed("True")
    assert sh.closed == True
    with pytest.raises(ValueError) as e:
        sh.set_closed("Yes it is")
    assert str(e.value) == "Value not recognised as True or False."


def test_add_ignoreProps(test_ShapeInfo: ShapeInfo):
    sh = test_ShapeInfo
    assert sh.ignoreProps == []
    sh.add_ignoreProps("rdf:type")
    assert sh.ignoreProps == ["rdf:type"]
    sh.add_ignoreProps("sdo:type")
    assert sh.ignoreProps == ["rdf:type", "sdo:type"]
    with pytest.raises(TypeError) as e:
        sh.add_ignoreProps(["dct:type"])
    assert str(e.value) == "Property id must be a string."
    assert sh.ignoreProps == ["rdf:type", "sdo:type"]
    sh.add_ignoreProps("dc:type, dct:type")
    assert sh.ignoreProps == ["rdf:type", "sdo:type", "dc:type", "dct:type"]


def test_set_mandatory(test_ShapeInfo: ShapeInfo):
    sh = test_ShapeInfo
    assert sh.mandatory == False
    sh.set_mandatory(True)
    assert sh.mandatory == True
    sh.set_mandatory(False)
    assert sh.mandatory == False
    sh.set_mandatory("True")
    assert sh.mandatory == True
    with pytest.raises(ValueError) as e:
        sh.set_mandatory("Nope")
    assert str(e.value) == "Value not recognised as True or False."


def test_set_severity(test_ShapeInfo: ShapeInfo):
    sh = test_ShapeInfo
    assert sh.severity == ""
    sh.set_severity("Violation")
    assert sh.severity == "violation"
    sh.set_severity("3")
    assert sh.severity == "3"
    with pytest.raises(TypeError) as e:
        sh.set_severity(3)
    assert str(e.value) == "Severity must be a string."


def test_add_note(test_ShapeInfo: ShapeInfo):
    sh = test_ShapeInfo
    assert sh.note == {}
    sh.add_note("en", "A Test")
    assert sh.note == {"en": "A Test"}
    sh.add_note("es", "Una Prueba")
    assert sh.note == {"en": "A Test", "es": "Una Prueba"}
    with pytest.raises(TypeError) as e:
        sh.add_note("en", 2)
    assert str(e.value) == "Language identifier and note must be strings."
    assert sh.note == {"en": "A Test", "es": "Una Prueba"}
    sh.add_note("en", "A Probe")
    assert sh.note == {"en": "A Probe", "es": "Una Prueba"}

def test_add_message(test_ShapeInfo: ShapeInfo):
    sh = test_ShapeInfo
    assert sh.messages == {}
    sh.add_message("en", "Something is wrong.")
    assert sh.messages["en"] == "Something is wrong."
    sh.add_message("es", "Algo es incorrecto.")
    assert sh.messages["en"] == "Something is wrong."
    assert sh.messages["es"] == "Algo es incorrecto."
    with pytest.raises(TypeError) as e:
        sh.add_message({"en": "type"})
    assert (
        str(e.value)[:60]
        == "ShapeInfo.add_message() missing 1 required positional argume"
    )
    with pytest.raises(TypeError) as e:
        sh.add_message("en", 2)
    assert (
        str(e.value) == "Language identifier and message must be strings."
    )
    with pytest.raises(TypeError) as e:
        sh.add_message(
            ["en", "es"], ["TType of resource.", "Tipo de recurso."]
        )
    assert (
        str(e.value) == "Language identifier and message must be strings."
    )
    assert sh.messages["en"] == "Something is wrong."
    assert sh.messages["es"] == "Algo es incorrecto."



def test_read_shapeInfoDict():
    fname = "tests/ap/TestData/shapes.csv"
    lang = "en"
    shapeDict = read_shapeInfoDict(fname, lang)
    assert len(shapeDict) == 2
    expectedShapeDict = {
        "BookShape": ShapeInfo(
            id="BookShape",
            label={"en": "Book"},
            comment={"en": "Shape for describing books"},
            targets={"class": ["sdo:Book", "ow:Work"]},
            closed=False,
            ignoreProps=[],
            mandatory=True,
            severity="violation",
            note={},
            messages={"en": "Error in Book data."}
        ),
        "AuthorShape": ShapeInfo(
            id="AuthorShape",
            label={"en": "Author"},
            comment={"en": "Shape for describing authors"},
            targets={"objectsof": ["dct:creator"], "class": ["sdo:Person"]},
            closed=True,
            ignoreProps=["rdf:type"],
            mandatory=False,
            severity="warning",
            note={},
        ),
    }
    assert shapeDict == expectedShapeDict
