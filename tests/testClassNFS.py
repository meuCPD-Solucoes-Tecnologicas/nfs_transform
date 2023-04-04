import unittest

from pyNFS import NFS
import os

class TestNFS_methods(unittest.TestCase):

    def testImport_xml_from_folder(self):
        with open("tests/xml/test.xml","rb") as fd:
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
        with open("tests/xml/nota_gerada.xml","r") as fd:
            xmloriginal = fd.read()
        xml = NFS.XMLPY(xmloriginal)
        xml.generate_NFeID()
        print(xml.id)
        dict = xml.getXMLDict()
        dict["NFe"]["infNFe"]["@Id"] = xml.id
        xml.setXMLDict(dict)
        xml.saveXML("tests/results/test3_nfe2_result.xml")
        cDV = xml.getXMLDict()["NFe"]["infNFe"]["ide"]["cDV"]

        
        #self.assertEqual(xml.id,"NFe352304463640580001155500100000270917009603388"+str(cDV))

    def testValidate_with_xsd(self):
        with open("tests/xml/nota_gerada.xml","r") as fd:
            xmloriginal = fd.read()
        xml = NFS.XMLPY(xmloriginal)
        
        #validate with folder /tests/xsds
        xsds = os.listdir("tests/xsds")
        with open("tests/results/corret_xsd.xml","w+") as fd:
            fd.write("VALIDATE WITH XSD\n")
        for xsd in xsds:
            with open("tests/results/corret_xsd.xml","a") as fd:
                fd.write("*"+str(xsd)+"* - ")
            try:
                xml.validate_with_xsd("tests/xsds/"+xsd,"tests/xml/nota_gerada.xml")
                with open("tests/results/corret_xsd.xml","a") as fd:
                    fd.write("SUCCESS \n")
                with open("tests/results/corret_xsd.xml","w+") as fd:
                    fd.write("Validated with xsd: "+xsd)
                validate = True
                break
            except Exception as e:
                validate = False
                with open("tests/results/corret_xsd.xml","a") as fd:
                    fd.write("FAILED \n\n ERROR: "+str(e)+"\n\n")

        self.assertEqual(validate,True)
           
                

            
        pass

    def testValidate_with_xsd_nfeProc(self):
        with open("tests/xml/nota_gerada.xml","r") as fd:
            xmloriginal = fd.read()
        xml = NFS.XMLPY(xmloriginal)
        
        #validate with folder /tests/xsds
        xsds = os.listdir("tests/xsds")
        with open("tests/results/corret_xsd.xml","w+") as fd:
            fd.write("VALIDATE WITH XSD\n")
       
        with open("tests/results/corret_xsd.xml","a") as fd:
            fd.write("*nfe_v4.00.xsd* - ")
        try:
            xml.validate_with_xsd("tests/xsds/nfe_v4.00.xsd","tests/xml/nota_gerada.xml")
            with open("tests/results/corret_xsd.xml","a") as fd:
                fd.write("SUCCESS \n")
            with open("tests/results/corret_xsd.xml","w+") as fd:
                fd.write("Validated with xsd: nfe_v4.00.xsd")
            validate = True
            
        except Exception as e:
            validate = False
            with open("tests/results/corret_xsd.xml","a") as fd:
                fd.write("FAILED \n\n ERROR: "+str(e)+"\n\n")

        self.assertEqual(validate,True)
           
                

            
        pass
    
    def testSign_cert(self):

        
        with open("tests/xml/nota_gerada.xml","r") as fd:
            xmloriginal = fd.read()
        xml = NFS.XMLPY(xmloriginal)
        xml.generate_NFeID()
        xml.setXML(xml.sign_procNfe("./NFS/certificados/LUZ_LED.p12"))
        xml.setXML(xml.getXML().replace("</NFe>",""))
        xml.setXML(xml.getXML().replace("</nfeProc>",""))
        xml.setXML(xml.getXML()+"</NFe></nfeProc>")

        xml.saveXML("tests/results/test4_nfe_result_signed.xml")
        pass
    
    def testGet_Json_of_XML(self):
        
        with open("tests/xml/nota_gerada.xml","r") as fd:
            xmloriginal = fd.read()
            xml = NFS.XMLPY(xmloriginal)
            with(open("tests/results/test_get_json_of_xml.json","w+")) as fd:
                fd.write(xml.get_Json())

    



        ...

    def testarEnviar_xml_de_NFe_complementar_homo(self):
        with open("tests/xml/Nota_valida.xml")as fd:
            xml = NFS.XMLPY(fd.read())

        xml.generate_NFeID()

        retorno=xml.enviar_nfe("./tests/xml/Nota_valida.xml",
                       "./NFS/certificados/LUZ_LED_NOVO.pfx")
        
        #carrega xml retorno

        xml_retorno= NFS.XMLPY(open(retorno,"r").read().replace("200\n",""))

        self.assertEqual(xml_retorno.getXMLDict()["soap:Envelope"]["soap:Body"]["nfeResultMsg"]["retEnviNFe"]["xMotivo"],"Lote recebido com sucesso")

        retorno = xml.consultar_nfe(str(self.id).replace("NFe",""),"tests/results/resposta.xml","NFS/certificados/LUZ_LED_NOVO.pfx")
        
        xml_retorno=NFS.XMLPY(retorno.text)

        self.assertNotEqual(xml_retorno.getXMLDict()["soap:Envelope"]["soap:Body"]["nfeResultMsg"]["retConsReciNFe"]["cStat"],"215")
        self.assertNotEqual(xml_retorno.getXMLDict()["soap:Envelope"]["soap:Body"]["nfeResultMsg"]["retConsReciNFe"]["cStat"],"656")
                  