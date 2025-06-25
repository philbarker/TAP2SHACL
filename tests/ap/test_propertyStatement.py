import pytest
from ap import AP, StatementTemplate


@pytest.fixture(scope="module")
def test_PS():
    ps = StatementTemplate()
    return ps


def test_add_property(test_PS):
    ps = test_PS
    assert ps.properties == []
    ps.add_property("rdf:type")
    assert ps.properties == ["rdf:type"]
    ps.add_property("dct:type")
    assert ps.properties == ["rdf:type", "dct:type"]
    with pytest.raises(TypeError) as e:
        ps.add_property(["sdo:additonalType"])
    assert str(e.value) == "Property identifier must be a string."
    assert ps.properties == ["rdf:type", "dct:type"]


def test_add_shape(test_PS):
    ps = test_PS
    assert ps.shapes == []
    ps.add_shape("Type")
    assert ps.shapes == ["Type"]
    ps.add_shape("Class")
    assert ps.shapes == ["Type", "Class"]
    with pytest.raises(TypeError) as e:
        ps.add_shape(["Additonal Type"])
    assert str(e.value) == "Shape identifier must be a string."
    assert ps.shapes == ["Type", "Class"]


def test_add_label(test_PS):
    ps = test_PS
    assert ps.labels == {}
    ps.add_label("en", "Type")
    assert ps.labels["en"] == "Type"
    ps.add_label("es", "Tipo")
    assert ps.labels["en"] == "Type"
    assert ps.labels["es"] == "Tipo"
    with pytest.raises(TypeError) as e:
        ps.add_label({"en": "type"})
    assert (
        str(e.value)[:60]
        == "StatementTemplate.add_label() missing 1 required positional "
    )
    with pytest.raises(TypeError) as e:
        ps.add_label("en", 2)
    assert str(e.value) == "Language identifier and label must be strings."
    with pytest.raises(TypeError) as e:
        ps.add_label(["en", "es"], ["type", "tipo"])
    assert str(e.value) == "Language identifier and label must be strings."
    assert ps.labels["en"] == "Type"
    assert ps.labels["es"] == "Tipo"


def test_add_mandatory(test_PS):
    ps = test_PS
    assert ps.mandatory == False
    ps.add_mandatory(True)
    assert ps.mandatory == True
    with pytest.raises(TypeError) as e:
        ps.add_mandatory(0)
    assert str(e.value) == "Mandatory must be set as boolean."
    assert ps.mandatory == True


def test_add_repeatable(test_PS):
    ps = test_PS
    assert ps.repeatable == True
    ps.add_repeatable(False)
    assert ps.repeatable == False
    with pytest.raises(TypeError) as e:
        ps.add_repeatable("True")
    assert str(e.value) == "Repeatable must be set as boolean."
    assert ps.repeatable == False


def test_add_valueNodeType(test_PS):
    ps = test_PS
    assert ps.valueNodeTypes == []
    ps.add_valueNodeType("IRI")
    assert ps.valueNodeTypes == ["IRI"]
    ps.add_valueNodeType("BNode")
    assert ps.valueNodeTypes == ["IRI", "BNode"]
    with pytest.raises(TypeError) as e:
        ps.add_valueNodeType(["URI", "Blank node"])
    assert str(e.value) == "Value node type must be a string."
    assert ps.valueNodeTypes == ["IRI", "BNode"]


def test_add_valueDataType(test_PS):
    ps = test_PS
    assert ps.valueDataTypes == []
    ps.add_valueDataType("xsd:string")
    assert ps.valueDataTypes == ["xsd:string"]
    ps.add_valueDataType("rdf:langString")
    assert ps.valueDataTypes == ["xsd:string", "rdf:langString"]
    with pytest.raises(TypeError) as e:
        ps.add_valueDataType(["rdf:HTML"])
    assert str(e.value) == "Value data type must be a string."
    assert ps.valueDataTypes == ["xsd:string", "rdf:langString"]


def test_add_valueConstraint(test_PS):
    ps = test_PS
    assert ps.valueConstraints == []
    ps.add_valueConstraint("ex:example")
    assert ps.valueConstraints == ["ex:example"]
    ps.add_valueConstraint(r"^http:\/\/example\.org/$")
    assert ps.valueConstraints == ["ex:example", r"^http:\/\/example\.org/$"]
    #    ps.add_valueConstraint("^\\d{3}-\\d{2}-\\d{4}$")
    #    assert "^\\d{3}-\\d{2}-\\d{4}$" in ps.valueConstraints
    with pytest.raises(TypeError) as e:
        ps.add_valueConstraint(["http://example.org/"])
    assert str(e.value) == "Constraint must be a string."


def test_add_valueConstraintType(test_PS):
    ps = test_PS
    assert ps.valueConstraintType == ""
    ps.add_valueConstraintType("pattern")
    assert ps.valueConstraintType == "pattern"
    ps.add_valueConstraintType("picklist")
    assert ps.valueConstraintType == "picklist"
    with pytest.raises(TypeError) as e:
        ps.add_valueConstraintType(None)
    assert str(e.value) == "Constraint type must be a string."
    assert ps.valueConstraintType == "picklist"


def test_add_valueShape(test_PS):
    ps = test_PS
    assert ps.valueShapes == []
    ps.add_valueShape("Person")
    assert ps.valueShapes == ["Person"]
    ps.add_valueShape("Organization")
    assert ps.valueShapes == ["Person", "Organization"]
    with pytest.raises(TypeError) as e:
        ps.add_valueShape(["Entity"])
    assert str(e.value) == "Shape must be a string."
    assert ps.valueShapes == ["Person", "Organization"]


def test_add_note(test_PS):
    ps = test_PS
    assert ps.notes == {}
    ps.add_note("en", "This is the type.")
    assert ps.notes["en"] == "This is the type."
    ps.add_note("es", "Este es el tipo.")
    assert ps.notes["en"] == "This is the type."
    assert ps.notes["es"] == "Este es el tipo."
    with pytest.raises(TypeError) as e:
        ps.add_note({"en": "type"})
    assert (
        str(e.value)[:60]
        == "StatementTemplate.add_note() missing 1 required positional a"
    )
    with pytest.raises(TypeError) as e:
        ps.add_note("en", 2)
    assert str(e.value) == "Language identifier and note must be strings."
    with pytest.raises(TypeError) as e:
        ps.add_note(["en", "es"], ["This is the type.", "Este es el tipo."])
    assert str(e.value) == "Language identifier and note must be strings."
    assert ps.notes["en"] == "This is the type."
    assert ps.notes["es"] == "Este es el tipo."


def test_add_severity(test_PS):
    ps = test_PS
    assert ps.severity == ""
    ps.add_severity("Warning")
    assert ps.severity == "Warning"
    ps.add_severity("Violation")
    assert ps.severity == "Violation"
    with pytest.raises(TypeError) as e:
        ps.add_severity(11)
    assert str(e.value) == "Severity value must be a string."
    assert ps.severity == "Violation"


def test_add_propertyDescription(test_PS):
    ps = test_PS
    assert ps.propertyDescriptions == {}
    ps.add_propertyDescription("en", "Type of resource.")
    assert ps.propertyDescriptions["en"] == "Type of resource."
    ps.add_propertyDescription("es", "Tipo de recurso.")
    assert ps.propertyDescriptions["en"] == "Type of resource."
    assert ps.propertyDescriptions["es"] == "Tipo de recurso."
    with pytest.raises(TypeError) as e:
        ps.add_propertyDescription({"en": "type"})
    assert (
        str(e.value)[:60]
        == "StatementTemplate.add_propertyDescription() missing 1 requir"
    )
    with pytest.raises(TypeError) as e:
        ps.add_propertyDescription("en", 2)
    assert (
        str(e.value) == "Language identifier and property description must be strings."
    )
    with pytest.raises(TypeError) as e:
        ps.add_propertyDescription(
            ["en", "es"], ["TType of resource.", "Tipo de recurso."]
        )
    assert (
        str(e.value) == "Language identifier and property description must be strings."
    )
    assert ps.propertyDescriptions["en"] == "Type of resource."
    assert ps.propertyDescriptions["es"] == "Tipo de recurso."

def test_add_propertyMessage(test_PS):
    ps = test_PS
    assert ps.message == {}
    ps.add_message("en", "Something is wrong.")
    assert ps.message["en"] == "Something is wrong."
    ps.add_message("es", "Algo es incorrecto.")
    assert ps.message["en"] == "Something is wrong."
    assert ps.message["es"] == "Algo es incorrecto."
    with pytest.raises(TypeError) as e:
        ps.add_message({"en": "type"})
    assert (
        str(e.value)[:60]
        == "StatementTemplate.add_message() missing 1 required positiona"
    )
    with pytest.raises(TypeError) as e:
        ps.add_message("en", 2)
    assert (
        str(e.value) == "Language identifier and message must be strings."
    )
    with pytest.raises(TypeError) as e:
        ps.add_message(
            ["en", "es"], ["TType of resource.", "Tipo de recurso."]
        )
    assert (
        str(e.value) == "Language identifier and message must be strings."
    )
    assert ps.message["en"] == "Something is wrong."
    assert ps.message["es"] == "Algo es incorrecto."

def test_result(test_PS):
    # integration test sum of all above
    ps = test_PS
    assert ps.properties == ["rdf:type", "dct:type"]
    assert ps.shapes == ["Type", "Class"]
    assert ps.labels["en"] == "Type"
    assert ps.labels["es"] == "Tipo"
    assert ps.mandatory == True
    assert ps.repeatable == False
    assert ps.valueNodeTypes == ["IRI", "BNode"]
    assert ps.valueDataTypes == ["xsd:string", "rdf:langString"]
    assert ps.valueConstraints == ["ex:example", r"^http:\/\/example\.org/$"]
    assert ps.valueConstraintType == "picklist"
    assert ps.valueShapes == ["Person", "Organization"]
    assert ps.notes["en"] == "This is the type."
    assert ps.notes["es"] == "Este es el tipo."
    assert ps.severity == "Violation"
    assert ps.propertyDescriptions["en"] == "Type of resource."
    assert ps.propertyDescriptions["es"] == "Tipo de recurso."
    assert ps.message["en"] == "Something is wrong."
    assert ps.message["es"] == "Algo es incorrecto."
    # which doesn't make much sense, but it is what we entered
