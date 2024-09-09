from dataclasses import dataclass, field, asdict
from .statementTemplate import StatementTemplate
from .shapeInfo import ShapeInfo, read_shapeInfoDict
from csv import DictReader
import pprint, re

defaultLang = "en"


@dataclass
class AP:
    """Data to define an Application Profile."""

    statementTemplates: list = field(default_factory=list)
    namespaces: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    shapeInfo: dict = field(default_factory=dict)

    def add_namespace(self, ns, uri):
        """Adds (over-writes) the ns: URI, key value pair to the namespaces dict."""
        if (type(ns) == str) and (type(uri) == str):
            if (len(ns) == 0) or ns == ":":
                prefix = "default"
            elif (ns[-1]) == ":":
                prefix = ns[:-1]
            else:
                prefix = ns
            self.namespaces[prefix] = uri
        else:
            msg = "Both ns and URI must be strings."
            raise TypeError(msg)
        return

    def add_metadata(self, prop, value):
        """Adds (over-writes) the ns: URI, key value pair to the namespaces dict."""
        if (type(prop) == str) and (type(value) == str):
            self.metadata[prop] = value
        else:
            msg = "Both ns and URI must be strings."
            raise TypeError(msg)
        return

    def add_shapeInfo(self, sh_id, sh_info):
        """Adds the info to the shape info dict."""
        if (type(sh_info) is ShapeInfo) and (type(sh_id) is str):
            self.shapeInfo[sh_id] = sh_info
        else:
            msg = "Info must be of ShapeInfo type, id must be a string."
            raise TypeError(msg)

    def add_statementTemplate(self, ps):
        """Adds StatementTemplate object to the list of property statements."""
        if ps in self.statementTemplates:
            pass
        elif type(ps) == StatementTemplate:
            self.statementTemplates.append(ps)
        else:
            msg = "Statement must be of StatementTemplate type."
            raise TypeError(msg)

    def load_namespaces(self, fname):
        """Load namespaces from a (csv) file."""
        # TODO could add options for loading from other formats
        with open(fname, "r") as csv_file:
            csvReader = DictReader(csv_file)
            for row in csvReader:
                if row["prefix"] and row["URI"]:
                    self.add_namespace(row["prefix"], row["URI"])
                elif row["URI"]:
                    self.add_namespace("", row["URI"])
                else:  # pass rows with missing data
                    pass

    def load_metadata(self, fname):
        """Load metadata from a (headingless csv) file."""
        # TODO could add options for loading from other formats
        # TODO option to have header row or not
        with open(fname, "r") as csv_file:
            csvReader = DictReader(csv_file, fieldnames=["key", "value"])
            for row in csvReader:
                self.add_metadata(row["key"], row["value"])

    def load_shapeInfo(self, fname):
        """Load shapeInfo from a (csv) file."""
        # TODO could add options for loading from other formats
        # TODO check shapeID column exists
        if ("lang" in self.metadata.keys()) and self.metadata["lang"]:
            lang = self.metadata["lang"]
        else:
            lang = defaultLang
        shapeInfoDict = read_shapeInfoDict(fname, lang)
        for key in shapeInfoDict.keys():
            self.add_shapeInfo(key, shapeInfoDict[key])

    def dump(self):
        """Print all the AP data."""
        pp = pprint.PrettyPrinter(indent=2)
        print("\n\n=== Metadata ===")
        pp.pprint(self.metadata)
        print("\n\n=== Namespaces ===")
        pp.pprint(self.namespaces)
        print("\n\n=== Shapes ===")
        pp.pprint(self.shapeInfo)
        print("\n\n=== statementTemplates ===")
        pp.pprint(self.statementTemplates)
        return
