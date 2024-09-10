Reads a Dublin Core [Tabular Application Profile](https://github.com/dcmi/dctap), with some extensions, and converts it to [SHACL](https://www.w3.org/TR/shacl/).

WARNING: beta version, use at own risk.

## Installation and use

Always install in a virtual environment (venv). Has several unstable dependencies (see below).

```
(venv) $ git clone https://github.com/philbarker/TAP2SHACL
(venv) $ cd TAP2SHACL
(venv) $ pip install -r requirements.txt
(venv) $ ./tap2shacl.py --help
```
usage: tap2shacl.py [-h] [-c <tap config file name>] [-ns <namespace csv file>]
                    [-a <tap metadata csv file>] [-s <shapes csv file>]
                    <tap csv file>

example: path/to/tap2shacl.py tap.csv

## Dependencies
tap2shacl used on several packages that deal with reading and processing the application profile:

* **APClasses** Provides python data classes for metadata application profiles, with methods to populate them.
* **dctap-python** Reads and carries out basic validation of a DCTAP instance. (This is a frozen version of [dctap-python](https://github.com/dcmi/dctap-python/))
* **TAP2AP** uses dctap-python to read a DC TAP (Dublin Core Tabular Application Profile), and some other config files, and converts it to a python application profile (APClasses).
* **AP2SHACL** exports the python application profile as SHACL.

Other dependencies are either from the python standard library (e.g. [urllib](https://docs.python.org/3/library/urllib.html), [csv](https://docs.python.org/3/library/csv.html)) or mature external packages (notably [rdflib](https://rdflib.readthedocs.io/en/stable/index.html)).
