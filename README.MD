Reads a Dublin Core [Tabular Application Profile](https://github.com/dcmi/dctap), with some extensions, and converts it to [SHACL](https://www.w3.org/TR/shacl/).

WARNING: alpha version, use at own risk.

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

example: ./tap2shacl.py examples/booksAP/tap.csv

## Dependencies
tap2shacl depends on several unstable packages that deal with reading and processing the application profile:

* [APClasses](https://github.com/philbarker/APClasses) Provides python data classes for metadata application profiles, with methods to populate them.
* [dctap-python](https://github.com/dcmi/dctap-python/) Reads and carries out basic validation of a DCTAP instance.
* [TAP2AP](https://github.com/philbarker/TAP2AP) uses dctap-python to read a DC TAP (Dublin Core Tabular Application Profile), and some other config files, and converts it to a python application profile (APClasses).
* [AP2SHACL](https://github.com/philbarker/AP2SHACL) exports the python application profile as SHACL.

Other dependencies are either from the python standard library (e.g. [urllib](https://docs.python.org/3/library/urllib.html), [csv](https://docs.python.org/3/library/csv.html)) or mature external packages (notably [rdflib](https://rdflib.readthedocs.io/en/stable/index.html)).
