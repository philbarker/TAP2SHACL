Reads a Dublin Core Tabular Application Profile, with some extensions, and converts it to SHACL.

WARNING: alpha version, use at own risk.

usage: tap2shacl.py [-h] [-c <tap config file name>] [-ns <namespace csv file>]
                    [-a <tap metadata csv file>] [-s <shapes csv file>]
                    <tap csv file>

example tap2shacl.py /tests/TestData/booksTAP.csv
