import xmltodict as xd
import xsd_validator as xsdV
import os
from lxml import etree
import json


class XMLPY:
    xml = ""
    xmldict = {}
    id = ""

    def __init__(self, xml: str):
        self.xml = xml
        self.xmldict = xd.parse(self.xml,force_list=('det',))
        

    def getXML(self):
        return self.xml

    def setXML(self, xml: str):
        self.xml = xml
        self.xmldict = xd.parse(self.xml)
            

    def getXMLDict(self):
        return self.xmldict

    def setXMLDict(self, xmldict: dict):
        self.xmldict = xmldict
        self.xml = xd.unparse(self.xmldict)
        

    def parseXML(self):
        return xd.parse(self.xml)
        

    def saveXML(self, filename: str):
        with open(filename, "w+") as fd:
            fd.write(self.xml)
        
    

    def get_Json(self):
        self.json = json.dumps(
            self.getXMLDict(), indent=4, sort_keys=True, ensure_ascii=False
        )
        return self.json
    