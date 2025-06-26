from dataclasses import dataclass, field, asdict


@dataclass
class StatementTemplate:
    """Data to define a Property Statement."""

    shapes: list = field(default_factory=list)
    properties: list = field(default_factory=list)
    labels: dict = field(default_factory=dict)
    mandatory: bool = False
    repeatable: bool = True
    valueNodeTypes: list = field(default_factory=list)
    valueDataTypes: list = field(default_factory=list)
    valueShapes: list = field(default_factory=list)
    valueClasses: list = field(default_factory=list)
    valueConstraints: list = field(default_factory=list)
    valueConstraintType: str = ""
    notes: dict = field(default_factory=dict)
    severity: str = ""
    message: dict = field(default_factory=dict)
    propertyDescriptions: dict = field(default_factory=dict)

    def add_property(self, propertyID):
        """Append propertyID to class properties list"""

        if type(propertyID) == str:
            if propertyID in self.properties:
                pass
            else:
                self.properties.append(propertyID)
        else:
            msg = "Property identifier must be a string."
            raise TypeError(msg)

    def add_shape(self, shapeID):
        """Append propertyID to class properties list"""

        if type(shapeID) == str:
            if shapeID in self.shapes:
                pass
            else:
                self.shapes.append(shapeID)
        else:
            msg = "Shape identifier must be a string."
            raise TypeError(msg)

    def add_label(self, lang, label):
        """Append {lang: label} to labels dict."""

        if (type(lang) == str) and (type(label) == str):
            self.labels[lang] = label
        else:
            msg = "Language identifier and label must be strings."
            raise TypeError(msg)

    def add_mandatory(self, man):
        """Set boolean value of mandatory to man."""
        if type(man) == bool:
            self.mandatory = man
        else:
            msg = "Mandatory must be set as boolean."
            raise TypeError(msg)

    def add_repeatable(self, rpt):
        """Set boolean value of repeatable to rpt."""
        if type(rpt) == bool:
            self.repeatable = rpt
        else:
            msg = "Repeatable must be set as boolean."
            raise TypeError(msg)

    def add_valueNodeType(self, vNT):
        """Append vNT to class valueNodeTypes list"""
        if type(vNT) == str:
            if vNT in self.valueNodeTypes:
                pass
            else:
                self.valueNodeTypes.append(vNT)
        else:
            msg = "Value node type must be a string."
            raise TypeError(msg)

    def add_valueDataType(self, vDT):
        """Append vDT to class valueDataTypes list"""
        if type(vDT) == str:
            if vDT in self.valueDataTypes:
                pass
            else:
                self.valueDataTypes.append(vDT)
        else:
            msg = "Value data type must be a string."
            raise TypeError(msg)

    def add_valueShape(self, shapeID):
        """Append shapeID to class valueShapes list"""
        if type(shapeID) == str:
            if shapeID in self.valueShapes:
                pass
            else:
                self.valueShapes.append(shapeID)
        else:
            msg = "Shape must be a string."
            raise TypeError(msg)

    def add_valueClass(self, classID):
        """Append classID to valueClasses list"""
        if type(classID) == str:
            if classID in self.valueClasses:
                pass
            else:
                self.valueClasses.append(classID)
        else:
            msg = "Class ID must be a string."
            raise TypeError(msg)

    def add_valueConstraint(self, constraint):
        """Append constraint to class valueConstraints list"""
        if type(constraint) == str:
            if constraint in self.valueConstraints:
                pass
            else:
                self.valueConstraints.append(constraint)
        else:
            msg = "Constraint must be a string."
            raise TypeError(msg)

    def add_valueConstraintType(self, constraintType):
        """Set (over-write) class valueConstraintType constraintType"""
        if type(constraintType) == str:
            self.valueConstraintType = constraintType
        else:
            msg = "Constraint type must be a string."
            raise TypeError(msg)

    def add_note(self, lang, note):
        """Append {lang: note} to notes dict."""
        if (type(lang) == str) and (type(note) == str):
            self.notes[lang] = note
        else:
            msg = "Language identifier and note must be strings."
            raise TypeError(msg)

    def add_severity(self, s):
        if type(s) == str:
            self.severity = s
        else:
            msg = "Severity value must be a string."
            raise TypeError(msg)

    def add_propertyDescription(self, lang, desc):
        """Append {lang: desc} to propertyDescription dict."""
        if (type(lang) == str) and (type(desc) == str):
            self.propertyDescriptions[lang] = desc
        else:
            msg = "Language identifier and property description must be strings."
            raise TypeError(msg)

    def add_message(self, lang, message):
        """Append {lang: note} to message dict."""
        if (type(lang) == str) and (type(message) == str):
            self.message[lang] = message
        else:
            msg = "Language identifier and message must be strings."
            raise TypeError(msg)
