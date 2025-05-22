from csv import DictReader
from dctap import csvreader  # , TAPShape, TAPStatementConstraint
from dctap.config import get_config
from ap import AP, StatementTemplate
import re

# defaults may be overridden by metadata file e.g. about.csv
default_language = "en-US"  # default language
# TODO read these from config
trueVals = ["true", "yes", "t", "y", "1"]  # probably not needed..
falseVals = ["false", "no", "f", "n", "0"]  # ... I think dctap normalises this
# chars used to separate multiple entries in cells
prop_splitters = ", |; |,|;| \n| |\n"
nodeType_splitters = ", |; |,|;| \n| |\n"
dataType_splitters = ", |; |,|;| \n| |\n"
constraint_splitters = ", |; |,|;| \n| |\n"
shape_splitters = ", |; |,|;| \n| |\n"


class TAP2APConverter:
    """Classs comprising AP and TAP data, with methods to convert latter to former"""

    def __init__(self, tap_fname, config_fname):
        self.ap = AP()
        self.tap = dict()
        self.tap["tap_fname"] = tap_fname
        self.tap["config_fname"] = config_fname
        self.load_tap(tap_fname, config_fname)

    def load_tap(self, tap_fname, config_fname):
        """Load TAP data from file."""
        self.tap["config_dict"] = get_config(nondefault_configfile_name=config_fname)
        with open(tap_fname, "r") as csv_fileObj:
            csvreader_output = csvreader(
                open_csvfile_obj=csv_fileObj, config_dict=self.tap["config_dict"]
            )
            self.tap["shapes_dict"] = csvreader_output
            self.tap["warnings_dict"] = csvreader_output["warnings"]

    def load_AP_Metadata(self, fname):
        self.ap.load_metadata(fname)

    def convert_TAP_AP(self):
        """Convert a TAP into python AP object."""
        shapes = self.tap["shapes_dict"]["shapes"]
        for shape in shapes:
            # check shapeID once and add it to all prop statements in shape
            sh_id = self.check_shapeID(shape["shapeID"])
            for sc in shape["statement_templates"]:
                ps = StatementTemplate()
                ps.add_shape(sh_id)
                # property ID is mandatory, no need to check for key
                self.convert_propertyIDs(sc["propertyID"], ps)
                if "propertyLabel" in sc.keys():
                    self.convert_labels(sc["propertyLabel"], ps)
                if "mandatory" in sc.keys():
                    self.convert_mandatory(sc["mandatory"], ps)
                if "repeatable" in sc.keys():
                    self.convert_repeatable(sc["repeatable"], ps)
                if "valueNodeType" in sc.keys():
                    self.convert_valueNodeTypes(sc["valueNodeType"], ps)
                if "valueDataType" in sc.keys():
                    self.convert_valueDataTypes(sc["valueDataType"], ps)
                if "valueConstraint" in sc.keys():
                    self.convert_valueConstraints(sc["valueConstraint"], ps)
                if "valueConstraintType" in sc.keys():
                    self.convert_valueConstraintType(sc["valueConstraintType"], ps)
                if "valueShape" in sc.keys():
                    self.convert_valueShapes(sc["valueShape"], ps)
                if "note" in sc.keys():
                    self.convert_notes(sc["note"], ps)
                if "severity" in sc.keys():
                    self.convert_severity(sc["severity"], ps)
                self.ap.add_statementTemplate(ps)

    def check_shapeID(self, sh_id):
        """Check a string matches a shape id."""
        # ShapeID should already be a key in shapeInfo
        # IDEA: could optionally add it if it is not.
        if type(sh_id) == str:
            pass
        else:
            msg = "shapeID must be a string."
            raise TypeError(msg)
        if sh_id in self.ap.shapeInfo.keys():
            pass
        else:
            msg = "No shape info for " + sh_id
            raise ValueError(msg)
        return sh_id

    def convert_propertyIDs(self, propertiesStr, ps):
        """Convert a string to a list of property ids, add them to a statementTemplate."""
        if type(propertiesStr) == str:
            for p in re.split(prop_splitters, propertiesStr):
                ps.add_property(p)
        else:
            msg = "Properties must be passed in a string."
            raise TypeError(msg)

    def convert_labels(self, label, ps):
        """Take string as label and add it to a statementTemplate."""
        # TODO: multiple labels, different languages
        try:
            lang = self.ap.metadata["language"]
        except (KeyError, ValueError):
            lang = default_language
        if type(label) == str:
            ps.add_label(lang, label)
        else:
            msg = "Labels must be passed in a string."
            raise TypeError(msg)

    def convert_mandatory(self, mandyStr, ps):
        """Convert a string to boolean true or false and add it as value of the `mandatory` property of statementTemplate."""
        if type(mandyStr) == str:
            if mandyStr.lower() in trueVals:
                ps.add_mandatory(True)
            elif mandyStr.lower() in falseVals:
                ps.add_mandatory(False)
            else:
                msg = "Value for mandatory not recognised: " + mandyStr
                raise ValueError(msg)
        else:
            msg = "Value for mandatory must be a string."
            raise TypeError(msg)

    def convert_repeatable(self, rptStr, ps):
        """Convert a string to boolean true or false and add it as value of the `repeatable` property of statementTemplate."""
        if type(rptStr) == str:
            if rptStr.lower() in trueVals:
                ps.add_repeatable(True)
            elif rptStr.lower() in falseVals:
                ps.add_repeatable(False)
            else:
                msg = "Value for repeatable not recognised: " + rptStr
                raise ValueError(msg)
        else:
            msg = "Value for repeatable must be a string."
            raise TypeError(msg)

    def convert_valueNodeTypes(self, nodeTypesStr, ps):
        """Convert a string of node types and into separate types and add them as values of the `valueNodeTypes` property of statementTemplate."""
        if type(nodeTypesStr) == str:
            for nodeType in re.split(nodeType_splitters, nodeTypesStr):
                ps.add_valueNodeType(nodeType)
        else:
            msg = "Value for node types must be a string."
            raise TypeError(msg)

    def convert_valueDataTypes(self, dataTypesStr, ps):
        """Convert a string of data types and into separate types and add them as values of the `valueNodeTypes` property of statementTemplate."""
        if type(dataTypesStr) == str:
            for dataType in re.split(dataType_splitters, dataTypesStr):
                ps.add_valueDataType(dataType)
        else:
            msg = "Value for data types must be a string."
            raise TypeError(msg)

    def convert_valueConstraints(self, constraints, ps):
        """Convert a constraint or list of constraints into separate items and add them as values of the `valueConstraints` property of statementTemplate."""
        # To do: dctap is now providing integer values for some constraints, cludgy patch included, but need to check details of what dctap is doing.
        if type(constraints) is str:
            for constraint in re.split(constraint_splitters, constraints):
                ps.add_valueConstraint(constraint)
        elif type(constraints) is int:
            constraint = str(constraints)
            ps.add_valueConstraint(constraint)
        elif type(constraints) is list:
            for list_item in constraints:
                if type(list_item) is str:
                    for constraint in re.split(constraint_splitters, list_item):
                        ps.add_valueConstraint(constraint)
                elif type(list_item) is int:
                    constraint = str(list_item)
                    ps.add_valueConstraint(constraint)
                else:
                    print(list_item)
                    msg = "Value for constraint must be a string or integer."
                    raise TypeError(msg)
        else:
            print(constraints)
            msg = "Value for constraints must be a string, integer or a list."
            raise TypeError(msg)

    def convert_valueConstraintType(self, constrTypeStr, ps):
        """Add a string as the value of the `valueConstraintType` property of statementTemplate."""
        if type(constrTypeStr) == str:
            ps.add_valueConstraintType(constrTypeStr)
        else:
            msg = "Value for constraint type must be a string."
            raise TypeError(msg)

    def convert_valueShapes(self, shapeStr, ps):
        """Convert a string of shapes into separate items and add them as values of the `valueShapes` property of statementTemplate."""

        if type(shapeStr) == str:
            for shape in re.split(shape_splitters, shapeStr):
                self.check_shapeID(shape)
                ps.add_valueShape(shape)
        else:
            msg = "Value for shapes must be a string."
            raise TypeError(msg)

    def convert_notes(self, noteStr, ps):
        """Take string as note and add it to a statementTemplate."""
        # TODO: multiple notes, different languages
        lang_keys = ["lang", "language", "dc:language", "dct:language"]
        if "lang" in self.ap.metadata.keys():
            lang = self.ap.metadata["lang"]
        elif "language" in self.ap.metadata.keys():
            lang = self.ap.metadata["language"]
        elif "dc:language" in self.ap.metadata.keys():
            lang = self.ap.metadata["dc:language"]
        elif "dct:language" in self.ap.metadata.keys():
            lang = self.ap.metadata["dct:language"]
        else:
            lang = default_language
        if type(noteStr) == str:
            ps.add_note(lang, noteStr)
        else:
            msg = "Notes must be passed in a string."
            raise TypeError(msg)

    def convert_severity(self, severityStr, ps):
        """Add a string as the value of the `severity` property of statementTemplate."""
        if type(severityStr) == str:
            ps.add_severity(severityStr)
        else:
            msg = "Value for severity must be a string."
            raise TypeError(msg)

    def convert_namespaces(self, source, fname=""):
        """Convert namespaces from TAP config file or load from AP csv."""
        if source == "TAP":
            prefixes = self.tap["config_dict"]["prefixes"]
            for prefix in prefixes:
                if (prefix != ":") and (prefix != ""):
                    if prefix[-1] == ":":  # ignore last char which is ":"
                        self.ap.add_namespace(prefix[:-1], prefixes[prefix])
                    else:
                        self.ap.add_namespace(prefix, prefixes[prefix])
                else:  # no prefix
                    self.ap.add_namespace("default", prefixes[prefix])
        elif source == "csv":
            self.ap.load_namespaces(fname)
        else:
            msg = 'source for namespaces must be "TAP" or "csv".'
            raise ValueError(msg)
