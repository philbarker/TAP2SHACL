from argparse import ArgumentParser

# defaults
tapFileName = "examples/bookAP/tap.csv"
configFileName = "dctap.yml"
namespaceFileName = "examples/bookAP/namespaces.csv"
aboutFileName = "examples/bookAP/about.csv"
shapesFileName = "examples/bookAP/shapes.csv"

def parse_arguments():
    parser = ArgumentParser(
        prog="tap2shacl.py",
        description="Reads a Dublin Core Tabular Application Profile, with some extensions, and converts it to SHACL."
    )
    parser.add_argument(
        "tapFileName",
        type=str,
        metavar='<tap csv file>'
    )
    parser.add_argument(
        "-c",
        "--configFileName",
        type=str,
        metavar='<tap config file name>',
        default=configFileName
    )
    parser.add_argument(
        "-ns",
        "--namespaceFileName",
        type=str,
        metavar='<namespace csv file>',
        default=namespaceFileName
    )
    parser.add_argument(
        "-a",
        "--aboutFileName",
        type=str,
        metavar='<tap metadata csv file>',
        default=aboutFileName
    )
    parser.add_argument(
        "-s",
        "--shapesFileName",
        type=str,
        metavar='<shapes csv file>',
        default=shapesFileName
    )
    return parser.parse_args()
