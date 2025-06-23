Reads a Dublin Core [Tabular Application Profile](https://github.com/dcmi/dctap), with some extensions, and converts it to [SHACL](https://www.w3.org/TR/shacl/).

WARNING: beta version, use at own risk.

## Installation and use

Always install in a virtual environment (venv).

`pip install tap2shacl` or install from github. 

```
(venv) $ git clone https://github.com/philbarker/TAP2SHACL
(venv) $ cd TAP2SHACL
(venv) $ pip install -r requirements.txt
(venv) $ ./tap2shacl.py --help
```
**usage:** `tap2shacl.py [-h] [-c «tap config file name»] [-ns «namespace csv file»]
                    [-a «tap metadata csv file»] [-s «shapes csv file»] -v
                    «tap csv file» [<output file>]`

example: `path/to/tap2shacl.py tap.csv shacl.ttl`

```
positional arguments:
  <tap csv file>
  <output file> (optional)
options
  -h, --help            show this help message and exit
  -c <tap config file name>, --configFileName <tap config file name>
  -ns <namespace csv file>, --namespaceFileName <namespace csv file>
  -a <tap metadata csv file>, --aboutFileName <tap metadata csv file>
  -s <shapes csv file>, --shapesFileName <shapes csv file>
  -v, --version         show program's version number and exit
```

If no output file is specified the output is written to the terminal.

## Contents
tap2shacl includes several modules that deal with reading and processing the application profile:

* **APClasses** Provides python data classes for metadata application profiles, with methods to populate them.
* **TAP2AP** uses dctap-python to read a DC TAP (Dublin Core Tabular Application Profile), and some other config files, and converts it to a python application profile (APClasses).
* **AP2SHACL** exports the python application profile as SHACL.

## Dependencies
Requires [dctap 0.4.5](https://pypi.org/project/dctap/)(alpha) ([github repo](https://github.com/dcmi/dctap-python)) which in turn introduces dependencies, notably ruamel.yaml 0.17.10.

Other dependencies are either from the python standard library (e.g. [dataclasses](https://docs.python.org/3/library/dataclasses.html), [urllib](https://docs.python.org/3/library/urllib.html), [csv](https://docs.python.org/3/library/csv.html)) or mature external packages (e.g. [rdflib](https://rdflib.readthedocs.io/en/stable/index.html)).
