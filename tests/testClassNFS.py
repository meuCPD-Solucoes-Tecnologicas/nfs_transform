import unittest

from pyNFS import NFS

class TestNFS_methods(unittest.TestCase):

    def testImport_xml_from_folder(self):
        with open("tests/xml/test.xml","r") as fd:
            xmloriginal = fd.read()
        xml = NFS.XMLPY(xmloriginal)
        self.assertEqual(xml.getXML(),xmloriginal)

    def testImport_xml_and_tranform_to_dict(self):
        with open("tests/xml/test.xml","r") as fd:
            xmloriginal = fd.read()
        xml = NFS.XMLPY(xmloriginal)
        print(xml.getXMLDict())
        self.assertEqual(xml.getXMLDict(),{'myxml': {'hello': 'world'}})
    
    def testImport_xml_and_modify_dict_save_and_get_again(self):
        with open("tests/xml/test.xml","r") as fd:
            xmloriginal = fd.read()
        xml = NFS.XMLPY(xmloriginal)
        xmldict = xml.getXMLDict()
        xmldict['myxml']['hello'] = 'world2'
        xml.setXMLDict(xmldict)
        self.assertEqual(xml.getXMLDict(),{'myxml': {'hello': 'world2'}})
        xml.saveXML("tests/xml/test2.xml")
        with open("tests/xml/test2.xml","r") as fd:
            xml2original = fd.read()
        xml2 = NFS.XMLPY(xml2original)
        self.assertEqual(xml2.getXMLDict(),{'myxml': {'hello': 'world2'}})

    def testGenerate_xml_id(self):
        with open("tests/xml/test3_nfe.xml","r") as fd:
            xmloriginal = fd.read()
        xml = NFS.XMLPY(xmloriginal)
        xml.generate_NFeID()
        print(xml.id)
        dict = xml.getXMLDict()
        dict["NFe"]["infNFe"]["@Id"] = xml.id
        xml.setXMLDict(dict)
        xml.saveXML("tests/results/test3_nfe2_result.xml")
        
        self.assertEqual(xml.id,"NFe35230346364058000115550020000415211184074372")
