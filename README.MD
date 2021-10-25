Reads a Dublin Core Tabular Application Profile, with some extensions, and converts it to SHACL.

WARNING: alpha version, use at own risk.

Installation

Always install in a virtual environment (venv). Has several unstable dependencies.

```
(venv) $ git clone https://github.com/philbarker/TAP2SHACL
(venv) $ cd TAP2SHACL
(venv) $ pip install -r requirements.txt
(venv) $ ./tap2shacl.py --help
```
usage: tap2shacl.py [-h] [-c <tap config file name>] [-ns <namespace csv file>]
                    [-a <tap metadata csv file>] [-s <shapes csv file>]
                    <tap csv file>

example: ./tap2shacl.py examples/booksTAP.csv
