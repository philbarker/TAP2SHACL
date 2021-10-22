from tap2ap import TAP2APConverter
from AP2SHACL import AP2SHACLConverter


class TAP2SHACLConverter:
    """Classs comprising TAP, AP data, with methods to convert from TAP to SHACL via AP"""

    def __init__(self, tap_fname, config_fname):
        self.tap2apConverter = TAP2APConverter(tap_fname, config_fname)
        self.tap = self.tap2apConverter.tap
        self.ap = self.tap2apConverter.ap
        self.ap2shaclConverter = AP2SHACLConverter(self.ap)
        self.sg = self.ap2shaclConverter.sg

    def convertTAP2AP(self, namespace_fname, about_fname, shapes_fname):
        self.tap2apConverter.convert_namespaces("TAP")
        self.tap2apConverter.convert_namespaces("csv", namespace_fname)
        self.tap2apConverter.ap.load_shapeInfo(shapes_fname)
        self.tap2apConverter.ap.load_metadata(about_fname)
        self.tap2apConverter.convert_TAP_AP()
        return self.tap2apConverter.ap

    def convertAP2SHACL(self):
        return self.ap2shaclConverter.convert_AP_SHACL()

    def dump_shacl(self):
        self.ap2shaclConverter.dump_shacl()

    def dump_ap(self):
        self.tap2apConverter.ap.dump()
