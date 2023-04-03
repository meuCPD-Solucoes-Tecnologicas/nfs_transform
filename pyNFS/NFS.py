import xmltodict as xd
from pynfe.processamento.assinatura import AssinaturaA1
import xsd_validator as xsdV
import os
from lxml import etree
import signxml
import pynfe.entidades as nfeent
import json


class XMLPY:
    xml = ""
    xmldict = {}
    id = ""

    def __init__(self, xml: str):
        self.xmlBytes=xml
        self.xml = xml
        self.xmldict = xd.parse(self.xml)
        pass

    @property
    def xml_lxml_etree_obj(self):
        """retorna o xml como objeto lxml.etree"""
        return etree.fromstring(self.xmlBytes)

    def getXML(self):
        return self.xml

    def setXML(self, xml: str):
        self.xml = xml
        self.xmlBytes=xml.encode()
        try:
            self.xmldict = xd.parse(self.xml)

        except:
            pass

    def getXMLDict(self):
        return self.xmldict

    def setXMLDict(self, xmldict: dict):
        self.xmldict = xmldict
        self.xml = xd.unparse(self.xmldict)
        self.xmlBytes=self.xml.encode()
        pass

    def parseXML(self):
        return xd.parse(self.xml)
        pass

    def saveXML(self, filename: str):
        with open(filename, "w+") as fd:
            fd.write(self.xml)
        pass

    def generate_NFeID(self):
        """A chave de acesso da nota fiscal é um identificador único da NF-e e é formada por uma sequência de 44 números que representam vários dados que identificam a nota fiscal e a empresa. Um template para a chave de acesso da nota fiscal poderia ser assim:


                cUF AAMM CNPJ mod série nNF tpEmis cNF cDV


                Onde:
                - cUF: código do estado onde está a empresa emitente da NF-e (2 dígitos)
                - AAMM: ano e mês da emissão da NF-e (4 dígitos)
                - CNPJ: CNPJ da empresa emitente (14 dígitos)
                - mod: identificação do modelo da NF-e (2 dígitos)
                - série: série da NF-e (3 dígitos)
                - nNF: número da nota fiscal eletrônica (9 dígitos)
                - tpEmis: tipo de emissão do documento (1 dígito)
                - cNF: código numérico da chave (8 dígitos)
                - cDV: dígito verificador da chave de acesso da NF-e (1 dígito)

                No entanto, é importante ressaltar que a geração de notas fiscais eletrônicas deve ser feita por meio de um sistema emissor autorizado pela Secretaria da Fazenda do seu estado. A chave de acesso é gerada automaticamente pelo sistema emissor de NF-e e é validada pela Secretaria da Fazenda no momento da autorização da nota fiscal.

                xml_base:
                <?xml version="1.0" encoding="UTF-8"?>
        <NFe xmlns="http://www.portalfiscal.inf.br/nfe">
            <infNFe versao="4.00" Id="NFe35230346364058000115550020000415211184074372">
                <ide>
                    <cUF>35</cUF>
                    <cNF>18407437</cNF>
                    <natOp>Complementar de ICMS (Serie 2)</natOp>
                    <mod>55</mod>
                    <serie>2</serie>
                    <nNF>41521</nNF>
                    <dhEmi>2023-03-21T16:19:42-03:00</dhEmi>
                    <tpNF>1</tpNF>
                    <idDest>2</idDest>
                    <cMunFG>3543907</cMunFG>
                    <tpImp>1</tpImp>
                    <tpEmis>1</tpEmis>
                    <cDV>2</cDV>
                    <tpAmb>1</tpAmb>
                    <finNFe>2</finNFe>
                    <indFinal>1</indFinal>
                    <indPres>2</indPres>
                    <indIntermed>0</indIntermed>
                    <procEmi>0</procEmi>
                    <verProc>Tiny ERP</verProc>
                    <NFref>
                        <refNFe>35220946364058000115550020000015761262368883</refNFe>
                    </NFref>
                </ide>
                <emit>
                    <CNPJ>46364058000115</CNPJ>
                    <xNome>LUZ LED COMERCIO ONLINE LTDA</xNome>
                    <xFant>LUZ LED DECOR</xFant>
                    <enderEmit>
                        <xLgr>Rua 7</xLgr>
                        <nro>192</nro>
                        <xCpl>Sala 02</xCpl>
                        <xBairro>Zona Central</xBairro>
                        <cMun>3543907</cMun>
                        <xMun>Rio Claro</xMun>
                        <UF>SP</UF>
                        <CEP>13500143</CEP>
                        <cPais>1058</cPais>
                        <xPais>Brasil</xPais>
                        <fone>1935571411</fone>
                    </enderEmit>
                    <IE>587462103112</IE>
                    <CRT>3</CRT>
                </emit>
                <dest>
                    <CPF>02771139030</CPF>
                    <xNome>Henrique Maia Braum</xNome>
                    <enderDest>
                        <xLgr>Rua Serafim Vargas</xLgr>
                        <nro>029</nro>
                        <xBairro>Morro do Espelho</xBairro>
                        <cMun>4318705</cMun>
                        <xMun>Sao Leopoldo</xMun>
                        <UF>RS</UF>
                        <CEP>93030210</CEP>
                        <cPais>1058</cPais>
                        <xPais>Brasil</xPais>
                    </enderDest>
                    <indIEDest>9</indIEDest>
                </dest>
                <det nItem="1">
                    <prod>
                        <cProd>CFOP6106</cProd>
                        <cEAN>SEM GTIN</cEAN>
                        <xProd>COMPLEMENTO DE ICMS</xProd>
                        <NCM>94053100</NCM>
                        <CFOP>6106</CFOP>
                        <uCom>UN</uCom>
                        <qCom>1.0000</qCom>
                        <vUnCom>0.00</vUnCom>
                        <vProd>0.00</vProd>
                        <cEANTrib>SEM GTIN</cEANTrib>
                        <uTrib>UN</uTrib>
                        <qTrib>1.0000</qTrib>
                        <vUnTrib>0.00</vUnTrib>
                        <indTot>1</indTot>
                    </prod>
                    <imposto>
                        <ICMS>
                            <ICMS00>
                                <orig>2</orig>
                                <CST>00</CST>
                                <modBC>1</modBC>
                                <vBC>49.90</vBC>
                                <pICMS>4.00</pICMS>
                                <vICMS>2.00</vICMS>
                            </ICMS00>
                        </ICMS>
                        <IPI>
                            <cEnq>999</cEnq>
                            <IPINT>
                                <CST>53</CST>
                            </IPINT>
                        </IPI>
                        <PIS>
                            <PISOutr>
                                <CST>49</CST>
                                <vBC>0.00</vBC>
                                <pPIS>0.00</pPIS>
                                <vPIS>0.00</vPIS>
                            </PISOutr>
                        </PIS>
                        <COFINS>
                            <COFINSOutr>
                                <CST>49</CST>
                                <vBC>0.00</vBC>
                                <pCOFINS>0.00</pCOFINS>
                                <vCOFINS>0.00</vCOFINS>
                            </COFINSOutr>
                        </COFINS>
                    </imposto>
                </det>
                <total>
                    <ICMSTot>
                        <vBC>49.90</vBC>
                        <vICMS>2.00</vICMS>
                        <vICMSDeson>0.00</vICMSDeson>
                        <vFCPUFDest>0.00</vFCPUFDest>
                        <vICMSUFDest>0.00</vICMSUFDest>
                        <vICMSUFRemet>0.00</vICMSUFRemet>
                        <vFCP>0.00</vFCP>
                        <vBCST>0.00</vBCST>
                        <vST>0.00</vST>
                        <vFCPST>0.00</vFCPST>
                        <vFCPSTRet>0.00</vFCPSTRet>
                        <vProd>0.00</vProd>
                        <vFrete>0.00</vFrete>
                        <vSeg>0.00</vSeg>
                        <vDesc>0.00</vDesc>
                        <vII>0.00</vII>
                        <vIPI>0.00</vIPI>
                        <vIPIDevol>0.00</vIPIDevol>
                        <vPIS>0.00</vPIS>
                        <vCOFINS>0.00</vCOFINS>
                        <vOutro>0.00</vOutro>
                        <vNF>0.00</vNF>
                    </ICMSTot>
                </total>
                <transp>
                    <modFrete>9</modFrete>
                    <vol>
                        <pesoL>0.000</pesoL>
                        <pesoB>0.000</pesoB>
                    </vol>
                </transp>
                <pag>
                    <detPag>
                        <tPag>90</tPag>
                        <vPag>0</vPag>
                    </detPag>
                </pag>
                <infAdic>
                    <infCpl>Conforme artigo 182 IV do RICMS, Nota fiscal complementar de ICMS
                        referente:&lt;br /&gt;A NF 1576 da serie 02 de 01/09/2022.</infCpl>
                </infAdic>
                <infRespTec>
                    <CNPJ>15088992000128</CNPJ>
                    <xContato>Fernando</xContato>
                    <email>integracao@tiny.com.br</email>
                    <fone>05430558200</fone>
                </infRespTec>
            </infNFe>
        </NFe>

        """

        # generate cUF AAMM CNPJ mod série nNF tpEmis cNF cDV
        cUF, AAMM, CNPJ, mod, serie, nNF, tpEmis, cNF, cDV = (
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        )
        # getcUF

        cUF = self.getXMLDict()["NFe"]["infNFe"]["ide"]["cUF"]

        # getAAMM

        AAMM = (
            self.getXMLDict()["NFe"]["infNFe"]["ide"]["dhEmi"][2:4]
            + self.getXMLDict()["NFe"]["infNFe"]["ide"]["dhEmi"][5:7]
        )

        # getCNPJ

        CNPJ = self.getXMLDict()["NFe"]["infNFe"]["emit"]["CNPJ"]

        # getmod

        mod = self.getXMLDict()["NFe"]["infNFe"]["ide"]["mod"]

        # getserie

        serie = str(
            self.getXMLDict()["NFe"]["infNFe"]["ide"]["serie"]
        ).zfill(3)

        # getnNF

        nNF = str(self.getXMLDict()["NFe"]["infNFe"]["ide"]["nNF"]).zfill(9)

        # gettpEmis

        tpEmis = self.getXMLDict()["NFe"]["infNFe"]["ide"]["tpEmis"]

        # getcNF

        cNF = self.getXMLDict()["NFe"]["infNFe"]["ide"]["cNF"]

        # getcDV and set cDV
        chave_withou_cDv=str(cUF + AAMM + CNPJ + mod + serie + nNF + tpEmis + cNF)
        cDV = self.calcula_cDV(chave_withou_cDv)
        cDV = str(cDV)
        dict=self.getXMLDict()
        dict["NFe"]["infNFe"]["ide"]["cDV"]=cDV
        dict["NFe"]["infNFe"]["@Id"] = "NFe" + cUF + AAMM + CNPJ + mod + serie + nNF + tpEmis + cNF + cDV
        self.setXMLDict(dict)

        # set id
        self.id = "NFe" + cUF + AAMM + CNPJ + mod + serie + nNF + tpEmis + cNF + cDV
        pass

    def validate_with_xsd(self, xsd_path, xml_path):
        # validate xsd_path exists

        if not os.path.exists(xsd_path):
            raise Exception("XSD file not found")
            pass
        # validate xml_path exists
        if not os.path.exists(xml_path):
            raise Exception("XML file not found")
            pass

        validator = xsdV.XsdValidator(xsd_path)
        validator.assert_valid(os.path.relpath(xml_path))
        pass

    def sign_procNfe(self, cert_file_path: str,senha="123456"):
        """
        Sign the xml file with the cert and key files

        Args:
            cert_file_path: o caminho do arquivo do certificado
            key_file: a file with the key

        Returns:
            _type_: string with the signed xml

        """
        
        a1 = AssinaturaA1(cert_file_path, senha)

        self.setXML(a1.assinar(self.xml_lxml_etree_obj, True).replace("\n", ""))

        self.setXML(self.xml.replace("</NFe>", ""))
        self.setXML(self.xml.replace("</nfeProc>", ""))
        self.setXML(
            """<?xml version="1.0" encoding="UTF-8"?>""" + self.xml + "</NFe>"
        )

        return self.xml

    def get_Json(self):
        self.json = json.dumps(
            self.getXMLDict(), indent=4, sort_keys=True, ensure_ascii=False
        )
        return self.json

    def enviar_nfe(self,xml_path):
        #enviar nfe para sefaz
        

        pass

    def calcula_cDV(self,chave: str) -> int:
        chave = [int(i) for i in chave]
        multiplicadores = [2, 3, 4, 5, 6, 7, 8, 9]
        soma = 0
        m = 0
        for i in range(len(chave)-1, -1, -1):
            soma += chave[i] * multiplicadores[m]
            m += 1
            if m > 7:
                m = 0
        resto = soma % 11
        if resto == 0 or resto == 1:
            cDV = 0
        else:
            cDV = 11 - resto
        return cDV