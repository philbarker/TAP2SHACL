#!/usr/bin/env python
from tap2shacl import TAP2SHACLConverter, TAP2APConverter, AP2SHACLConverter
from parseArguments import parse_arguments

if __name__ == "__main__":
    args = parse_arguments()
    print(args.tapFileName)
    tapFName = args.tapFileName
    c = TAP2SHACLConverter(tapFName, args.configFileName)
    c.convertTAP2AP(args.namespaceFileName, args.aboutFileName, args.shapesFileName)
    c.convertAP2SHACL()
    #    c.dump_ap()
    c.dump_shacl(args.outputFileName)
