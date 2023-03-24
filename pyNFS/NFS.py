import xmltodict as xd

class XMLPY:
    xml=""
    xmldict={}
    def __init__ (self, xml:str):
        self.xml = xml
        self.xmldict = xd.parse(self.xml)
        pass
    
    def getXML(self):
        return self.xml
    
    def setXML(self, xml:str):
        self.xml = xml
    
    def getXMLDict(self):
        return self.xmldict
    
    def setXMLDict(self, xmldict:dict):

        self.xmldict = xmldict
        self.xml = xd.unparse(self.xmldict)
        pass

    
    def parseXML(self):
        return xd.parse(self.xml)
        pass

    def saveXML(self, filename:str):
        with open(filename,"w+") as fd:
            fd.write(self.xml)
        pass


