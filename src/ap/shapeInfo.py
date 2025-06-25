from dataclasses import dataclass, field, asdict
from csv import DictReader
import re

# TODO read these from config
# chars used to separate multiple entries in cells
target_splitters = ", |; |,|;| \n| |\n"


def read_shapeInfoDict(fname, lang):
    """Read data from a (csv) file, return a list of ShapeInfo objects."""
    # TODO could add options for loading from other formats
    shapeInfoDict = {}
    with open(fname, "r") as csv_file:
        csvReader = DictReader(csv_file)
        for row in csvReader:
            if row["shapeID"]:
                id = row["shapeID"]
                if id in shapeInfoDict.keys():
                    s = shapeInfoDict[id]
                else:
                    s = ShapeInfo()
                s.set_id(id)
                if ("label" in row.keys()) and row["label"]:
                    s.add_label(lang, row["label"])
                if ("comment" in row.keys()) and row["comment"]:
                    s.add_comment(lang, row["comment"])
                if (
                    ("target" in row.keys())
                    and row["target"]
                    and ("targetType" in row.keys())
                    and row["targetType"]
                ):
                    s.append_target(row["target"], row["targetType"])
                if ("closed" in row.keys()) and row["closed"]:
                    s.set_closed(row["closed"])
                if ("ignoreProps" in row.keys()) and row["ignoreProps"]:
                    s.add_ignoreProps(row["ignoreProps"])
                if ("mandatory" in row.keys()) and row["mandatory"]:
                    s.set_mandatory(row["mandatory"])
                if ("severity" in row.keys()) and row["severity"]:
                    s.set_severity(row["severity"])
                if ("note" in row.keys()) and row["note"]:
                    s.add_note(lang, row["note"])
                if ("message" in row.keys()) and row["message"]:
                    s.add_message(lang, row["message"])
                shapeInfoDict[id] = s
            else:  # skip lines with no shape id
                continue
    return shapeInfoDict


@dataclass
class ShapeInfo:
    """Data with information about a shape."""

    id: str = ""
    label: dict = field(default_factory=dict)
    comment: dict = field(default_factory=dict)
    targets: list = field(default_factory=dict)
    closed: bool = False
    ignoreProps: list = field(default_factory=list)
    mandatory: bool = False
    severity: str = ""
    message: dict = field(default_factory=dict)
    note: dict = field(default_factory=dict)

    def set_id(self, id):
        """Set the value of shapeID to be the id."""

        if type(id) == str:
            self.id = id
        else:
            msg = "Shape identifier must be a string."
            raise TypeError(msg)

    def add_label(self, lang, label):
        """Add {lang: label} to label dict."""

        if (type(lang) == str) and (type(label) == str):
            self.label[lang] = label
        else:
            msg = "Language identifier and label must be strings."
            raise TypeError(msg)

    def add_comment(self, lang, label):
        """Add {lang: label} to comments dict."""

        if (type(lang) == str) and (type(label) == str):
            self.comment[lang] = label
        else:
            msg = "Language identifier and comment must be strings."
            raise TypeError(msg)

    def append_target(self, target, target_type):
        """Append {target_type: target} to targets dict."""
        known_types = ["class", "instance", "objectsof", "subjectsof"]
        if (type(target) == str) and (type(target_type) == str):
            lc_target_type = target_type.lower()
            if lc_target_type in self.targets.keys():
                for t in re.split(target_splitters, target):
                    self.targets[lc_target_type].append(t)
            elif lc_target_type in known_types:
                self.targets[lc_target_type] = list()
                for t in re.split(target_splitters, target):
                    self.targets[lc_target_type].append(t)
            else:
                self.targets[target_type] = target
                msg = "Warning, ", target_type, " is unknown."
                print(msg)
        else:
            msg = "Target and type must be strings."
            raise TypeError(msg)

    def set_closed(self, isClosed):
        """Set boolean value of closed to value of isClosed"""
        # To do: option to set these in AP
        t_vals = ["true", "t", "yes", "y", "1"]
        f_vals = ["false", "f", "no", "n", "0"]
        if str(isClosed).lower() in t_vals:
            self.closed = True
        elif str(isClosed).lower() in f_vals:
            self.closed = False
        else:
            msg = "Value not recognised as True or False."
            raise ValueError(msg)

    def add_ignoreProps(self, properties):
        """Set list of properties to ignore from string properties"""
        splitters = ", |; |,|;| \n| |\n"  # ideally read from config
        if type(properties) == str:
            value_list = re.split(splitters, properties)
            self.ignoreProps.extend(value_list)
        else:
            msg = "Property id must be a string."
            raise TypeError(msg)

    def set_mandatory(self, isMandatory):
        """Set boolean value of closed to value of isClosed"""
        # To do: option to set these in AP
        t_vals = ["true", "t", "yes", "y", "1"]
        f_vals = ["false", "f", "no", "n", "0"]
        if str(isMandatory).lower() in t_vals:
            self.mandatory = True
        elif str(isMandatory).lower() in f_vals:
            self.mandatory = False
        else:
            msg = "Value not recognised as True or False."
            raise ValueError(msg)

    def set_severity(self, severity):
        """Append {target_type: target} to targets dict."""
        known_vals = ["warning", "info", "violation", ""]
        if type(severity) == str:
            if severity.lower() in known_vals:
                self.severity = severity.lower()
            else:
                self.severity = severity.lower()
                msg = "Warning, severity", severity, " is unknown."
                print(msg)
        else:
            msg = "Severity must be a string."
            raise TypeError(msg)

    def add_note(self, lang, note):
        """Add {lang: label} to note dict."""

        if (type(lang) == str) and (type(note) == str):
            self.note[lang] = note
        else:
            msg = "Language identifier and note must be strings."
            raise TypeError(msg)

    def add_message(self, lang, message):
        """Append {lang: note} to message dict."""
        if (type(lang) == str) and (type(message) == str):
            self.message[lang] = message
        else:
            msg = "Language identifier and message must be strings."
            raise TypeError(msg)