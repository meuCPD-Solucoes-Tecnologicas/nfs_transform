
import os, sys
from pyNFS import NFS as nfs
from datetime import datetime
from pytz import timezone
def main(argv):


    #definição de variaveis pasta de nfs originais e nfs complementares (geradas)
    sourceFolder=os.path.relpath(argv[0])
    targetFolder=os.path.relpath(argv[1])
    baseFOlder=os.path.relpath(argv[2])

    #verifica se a pasta de origem existe
    if not os.path.exists(sourceFolder):
        print("Pasta de origem não encontrada")
        sys.exit(1)
    
    #verifica se a pasta de destino existe
    if not os.path.exists(targetFolder):
        print("Pasta de destino não encontrada")
        sys.exit(1)

    #verifica se a pasta de base existe
    if not os.path.exists(baseFOlder):
        print("Pasta de base não encontrada")
        sys.exit(1)
    
    #verifica se a pasta de origem está vazia
    if not os.listdir(sourceFolder):
        print("Pasta de origem vazia")
        sys.exit(1)

    #lista de arquivos xml na pasta de origem
    xmlFiles = [f for f in os.listdir(sourceFolder) if f.endswith('.xml')]
    print("Arquivos Encontrados:")
    for xmlfile in xmlFiles:
        print(xmlfile)
    pass


    print("Transformando Complementares:")
    nNFE=2708
    for xmlarqs in xmlFiles:
        originalXML = nfs.XMLPY(open(os.path.join(sourceFolder,xmlarqs),'r').read())
        complemenatarXML = nfs.XMLPY(open(os.path.join(baseFOlder,"base.xml"),'r').read())
        #####################################################################################
        # Referencia da complementar na nf original

        dict = complemenatarXML.getXMLDict()
        complemenatarXML.getXMLDict()["NFe"]["infNFe"]["ide"]["NFref"]["refNFe"] =str(originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']["@Id"]).replace("NFe","")
        complemenatarXML.setXMLDict(dict)
        
        #nNF da complementar
        #começa em 2708 com 6 digitos e vai incrementando
        dict = complemenatarXML.getXMLDict()
        complemenatarXML.getXMLDict()["NFe"]["infNFe"]["ide"]["nNF"] = str(nNFE).zfill(6)
        nNFE+=1
        complemenatarXML.setXMLDict(dict)

        #definir data de emissão da complementar
        # Definir o fuso horário
        tz = timezone('America/Sao_Paulo')

        # Obter a data e hora atual no fuso horário especificado
        now = datetime.now(tz)

        # Formatar a data e hora no formato desejado
        formatted_date = now.strftime('%Y-%m-%dT%H:%M:%S%z')

        dict = complemenatarXML.getXMLDict()
        complemenatarXML.getXMLDict()["NFe"]["infNFe"]["ide"]["dhEmi"] = formatted_date
        complemenatarXML.setXMLDict(dict)

        #cNF e cDV da complementar

        dict = complemenatarXML.getXMLDict()

        complemenatarXML.getXMLDict()["NFe"]["infNFe"]["ide"]["cNF"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['cNF']
        complemenatarXML.getXMLDict()["NFe"]["infNFe"]["ide"]["cDV"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['cDV']

        # Complemento de ICMS
        dict = complemenatarXML.getXMLDict()
        #save original value on file
        with open(os.path.join(targetFolder,"originalvalue.py"),'w+') as fd:
            fd.write(str(complemenatarXML.getXMLDict())+'\n')
        try:
            #print(originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det']['prod'])
            dict['NFe']['infNFe']["det"]["imposto"]["ICMS"]["ICMS00"]["vBC"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det']['prod']['vProd']
            dict['NFe']['infNFe']["total"]["ICMSTot"]["vBC"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det']['prod']['vProd']
            dict['NFe']['infNFe']["det"]["prod"]["NCM"]=originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det']['prod']['NCM']
        except: 
            #print(originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det'][0]['prod'])
            print("VPROD EM LISTA")
            dict['NFe']['infNFe']["det"]["imposto"]["ICMS"]["ICMS00"]["vBC"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det'][0]['prod']['vProd']
            dict['NFe']['infNFe']["total"]["ICMSTot"]["vBC"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det'][0]['prod']['vProd']
            dict['NFe']['infNFe']["det"]["prod"]["NCM"]=originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det'][0]['prod']['NCM']

        complemenatarXML.setXMLDict(dict)

        #  Complemento de CONFINS
        dict = complemenatarXML.getXMLDict()
        try:
            dict['NFe']['infNFe']["det"]["imposto"]["COFINS"]["COFINSOutr"]["vBC"] = 0.0
            dict['NFe']['infNFe']["det"]["imposto"]["COFINS"]["COFINSOutr"]["pCOFINS"] = 0.0
            dict['NFe']['infNFe']["det"]["imposto"]["COFINS"]["COFINSOutr"]["vCOFINS"] = 0.0
            dict['NFe']['infNFe']["det"]["imposto"]["PIS"]["PISOutr"]["vBC"] = 0.0
            dict['NFe']['infNFe']["det"]["imposto"]["PIS"]["PISOutr"]["pPIS"] = 0.0
            dict['NFe']['infNFe']["det"]["imposto"]["PIS"]["PISOutr"]["vPIS"] = 0.0
        except:
            print("VBC EM LISTA")
            dict['NFe']['infNFe']["det"][0]["imposto"]["COFINS"]["COFINSOutr"]["vBC"] = 0.0
            dict['NFe']['infNFe']["det"][0]["imposto"]["COFINS"]["COFINSOutr"]["pCOFINS"] = 0.0
            dict['NFe']['infNFe']["det"][0]["imposto"]["COFINS"]["COFINSOutr"]["vCOFINS"] = 0.0
            dict['NFe']['infNFe']["det"][0]["imposto"]["PIS"]["PISOutr"]["vBC"] = 0.0
            dict['NFe']['infNFe']["det"][0]["imposto"]["PIS"]["PISOutr"]["pPIS"] = 0.0
            dict['NFe']['infNFe']["det"][0]["imposto"]["PIS"]["PISOutr"]["vPIS"] = 0.0
        complemenatarXML.setXMLDict(dict)

        # ICMS Total
        dict = complemenatarXML.getXMLDict()
        try:
            dict['NFe']['infNFe']["total"]["ICMSTot"]["vICMS"] = round(float(complemenatarXML.getXMLDict()['NFe']['infNFe']["det"]["imposto"]["ICMS"]["ICMS00"]["vBC"]) * 0.04,2)
            complemenatarXML.getXMLDict()['NFe']['infNFe']["det"]["imposto"]["ICMS"]["ICMS00"]["vICMS"] = round(float(complemenatarXML.getXMLDict()['NFe']['infNFe']["det"]["imposto"]["ICMS"]["ICMS00"]["vBC"]) * 0.04,2)
        except Exception as e:
            print(e)
            dict['NFe']['infNFe']["total"]["ICMSTot"]["vICMS"] = round(float(complemenatarXML.getXMLDict()['NFe']['infNFe']["det"][0]["imposto"]["ICMS"]["ICMS00"]["vBC"]) * 0.04,2)
            complemenatarXML.getXMLDict()['NFe']['infNFe']["det"]["imposto"]["ICMS"]["ICMS00"]["vICMS"] = round(float(complemenatarXML.getXMLDict()['NFe']['infNFe']["det"][0]["imposto"]["ICMS"]["ICMS00"]["vBC"]) * 0.04,2)
        complemenatarXML.setXMLDict(dict)

        #  InfADIC
        dict = complemenatarXML.getXMLDict()

        valores={'data-emissao': originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['dhEmi'],
                 "No_NF": originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['nNF'],
                 "serie": originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['serie']}
        texto=f"""
        Conforme artigo 182 IV do RICMS, Nota fiscal complementar de ICMS referente a NF "*{valores["No_NF"]}*" da serie "*{str(valores["serie"]).zfill(2)}*" de "*{datetime.strptime(valores["data-emissao"].split("T")[0].replace("-","/"),"%Y/%m/%d").strftime("%d/%m/%Y")}*".
        """
        dict['NFe']['infNFe']["infAdic"]["infCpl"] = texto
        dict['NFe']['infNFe']["ide"]["serie"] = valores['serie']
        dict['NFe']['infNFe']["ide"]["natOp"] = f"Complementar de ICMS (Serie {valores['serie']})"
        
        if(valores['serie'] == '1'):
            try:
                dict['NFe']['infNFe']["det"]["prod"]["CFOP"] = '6108'
            except:
                dict['NFe']['infNFe']["det"][0]["prod"]["CFOP"] = '6108'
        elif(valores['serie'] == '2'):
            try:
                dict['NFe']['infNFe']["det"]["prod"]["CFOP"] = '6106'
            except:
                dict['NFe']['infNFe']["det"][0]["prod"]["CFOP"] = '6106'



        complemenatarXML.setXMLDict(dict)

        #emit 

        """
        complemantar
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
                
                original
                <emit>
                <CNPJ>46364058000115</CNPJ>
                <xNome>LUZ LED COMERCIO ONLINE LTDA</xNome>
                <enderEmit>
                    <xLgr>Avenida 59</xLgr>
                    <nro>1513</nro>
                    <xBairro>Jardim Anhanguera</xBairro>
                    <cMun>3543907</cMun>
                    <xMun>Rio Claro</xMun>
                    <UF>SP</UF>
                    <CEP>13501560</CEP>
                    <cPais>1058</cPais>
                    <xPais>Brasil</xPais>
                    <fone>001935571411</fone>
                </enderEmit>
                <IE>587462103112</IE>
                <CRT>1</CRT>
            </emit>
                """
        dict = complemenatarXML.getXMLDict()
        dict['NFe']['infNFe']["emit"]["CNPJ"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['CNPJ']
        dict['NFe']['infNFe']["emit"]["xNome"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['xNome']
        dict['NFe']['infNFe']["emit"]["enderEmit"]["xLgr"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['xLgr']
        dict['NFe']['infNFe']["emit"]["enderEmit"]["nro"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['nro']
        dict['NFe']['infNFe']["emit"]["enderEmit"]["xBairro"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['xBairro']
        dict['NFe']['infNFe']["emit"]["enderEmit"]["cMun"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['cMun']
        dict['NFe']['infNFe']["emit"]["enderEmit"]["xMun"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['xMun']
        dict['NFe']['infNFe']["emit"]["enderEmit"]["UF"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['UF']
        dict['NFe']['infNFe']["emit"]["enderEmit"]["CEP"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['CEP']
        dict['NFe']['infNFe']["emit"]["enderEmit"]["cPais"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['cPais']
        dict['NFe']['infNFe']["emit"]["enderEmit"]["xPais"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['xPais']
        dict['NFe']['infNFe']["emit"]["enderEmit"]["fone"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['fone']
        dict['NFe']['infNFe']["emit"]["IE"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['IE']
        dict['NFe']['infNFe']["emit"]["CRT"] = 3#originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['CRT']

        complemenatarXML.setXMLDict(dict)

        #dest
        """complementar
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

            original
             <dest>
                <CPF>02771139030</CPF>
                <xNome>Henrique Maia Braum</xNome>
                <enderDest>
                    <xLgr>Rua Serafim Vargas</xLgr>
                    <nro>29</nro>
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

        """
        dict = complemenatarXML.getXMLDict()

        dict['NFe']['infNFe']["dest"]["CPF"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['CPF']
        dict['NFe']['infNFe']["dest"]["xNome"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['xNome']
        dict['NFe']['infNFe']["dest"]["enderDest"]["xLgr"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['xLgr']
        dict['NFe']['infNFe']["dest"]["enderDest"]["nro"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['nro']
        dict['NFe']['infNFe']["dest"]["enderDest"]["xBairro"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['xBairro']
        dict['NFe']['infNFe']["dest"]["enderDest"]["cMun"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['cMun']
        dict['NFe']['infNFe']["dest"]["enderDest"]["xMun"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['xMun']
        dict['NFe']['infNFe']["dest"]["enderDest"]["UF"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['UF']
        dict['NFe']['infNFe']["dest"]["enderDest"]["CEP"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['CEP']
        dict['NFe']['infNFe']["dest"]["enderDest"]["cPais"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['cPais']
        dict['NFe']['infNFe']["dest"]["enderDest"]["xPais"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['xPais']
        dict['NFe']['infNFe']["dest"]["indIEDest"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['indIEDest']

        complemenatarXML.setXMLDict(dict)
        

        # gerar o id da nota
        dict = complemenatarXML.getXMLDict()
        complemenatarXML.generate_NFeID()
        dict["NFe"]["infNFe"]["@Id"] = complemenatarXML.id
        complemenatarXML.setXMLDict(dict)

        #####################################################################################
        print(complemenatarXML.getXMLDict()["NFe"]["infNFe"]["@Id"])
        complemenatarXML.saveXML(os.path.join(targetFolder,xmlarqs.split("-")[0]+" - COMPLEMENTAR - "+complemenatarXML.getXMLDict()["NFe"]["infNFe"]["ide"]["NFref"]["refNFe"]+'.xml'))

if __name__ == '__main__':
    main(sys.argv[1:])