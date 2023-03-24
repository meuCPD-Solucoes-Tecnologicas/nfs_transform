"""
    Esse arquivo python tem como objetivo utilizar o pacote pyNFS para
    realizar a leitura de arquivos XML e modificalos, gerando assim um nota fiscal
    complementar.

    Teremos como base o arquivo xml de exemplo de nf complementar, que está na pasta NFS/Base
    sendo assim vamos receber uma nf original e gerar uma nf complementar a partir dela.

    devemos seguir os seguintes passos:

    1 - Referencia da complementar na nf original 
        <NFref>
                    <refNFe>[infNFe Id complementar]</refNFe>
        </NFref>
        então usar esse id para gerar a nf complementar.

    2 - Complemento de ICMS

        - <prod> é o mesmo para todos
        - <prod><NCM> é o mesmo para todos
        - <ICMS00><vBC> esse valor vai ser colocado em:
            <prod><vprod>
             <PIS><PISOutr><vBC>
    
    3 - Complemento de CONFINS
        zerar <vBC> ,<pCOFINS>  e <vCOFINS>
         <COFINS>
                        <COFINSOutr>
                            <CST>49</CST>
                            <vBC>49.90</vBC>
                            <pCOFINS>0.0000</pCOFINS>
                            <vCOFINS>0.00</vCOFINS>
                        </COFINSOutr>
                    </COFINS>

    4 - <total>
                <ICMSTot><vICMS> = <vBC> * 4%

    5 - <infAdic><infCpl> mudar dentro da string série , número e data de emissão conforme nf original

    6 - remover <signature> e <infNFeSupl>
        
"""
import os, sys
from pyNFS import NFS as nfs
from datetime import datetime
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
    for xmlarqs in xmlFiles:
        originalXML = nfs.XMLPY(open(os.path.join(sourceFolder,xmlarqs),'r').read())
        complemenatarXML = nfs.XMLPY(open(os.path.join(baseFOlder,"base.xml"),'r').read())
        #####################################################################################
        # 1 - Referencia da complementar na nf original

        dict = complemenatarXML.getXMLDict()
        dict['NFe']['infNFe']['@Id'] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']["NFref"]["refNFe"]
        complemenatarXML.setXMLDict(dict)

        # 2 - Complemento de ICMS
        dict = complemenatarXML.getXMLDict()
        #save original value on file
        with open(os.path.join(targetFolder,"originalvalue.py"),'w+') as fd:
            fd.write(str(complemenatarXML.getXMLDict())+'\n')
        try:
            #print(originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det']['prod'])
            dict['NFe']['infNFe']["det"]["imposto"]["ICMS"]["ICMS00"]["vBC"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det']['prod']['vProd']
            dict['NFe']['infNFe']["total"]["ICMSTot"]["vBC"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det']['prod']['vProd']
        except: 
            #print(originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det'][0]['prod'])
            print("VPROD EM LISTA")
            dict['NFe']['infNFe']["det"]["imposto"]["ICMS"]["ICMS00"]["vBC"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det'][0]['prod']['vProd']
            dict['NFe']['infNFe']["total"]["ICMSTot"]["vBC"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det'][0]['prod']['vProd']

        complemenatarXML.setXMLDict(dict)

        # 3 - Complemento de CONFINS
        dict = complemenatarXML.getXMLDict()
        try:
            dict['NFe']['infNFe']["det"]["imposto"]["COFINS"]["COFINSOutr"]["vBC"] = 0
            dict['NFe']['infNFe']["det"]["imposto"]["COFINS"]["COFINSOutr"]["pCOFINS"] = 0
            dict['NFe']['infNFe']["det"]["imposto"]["COFINS"]["COFINSOutr"]["vCOFINS"] = 0
            dict['NFe']['infNFe']["det"]["imposto"]["PIS"]["PISOutr"]["vBC"] = 0
            dict['NFe']['infNFe']["det"]["imposto"]["PIS"]["PISOutr"]["pPIS"] = 0
            dict['NFe']['infNFe']["det"]["imposto"]["PIS"]["PISOutr"]["vPIS"] = 0
        except:
            print("VBC EM LISTA")
            dict['NFe']['infNFe']["det"][0]["imposto"]["COFINS"]["COFINSOutr"]["vBC"] = 0
            dict['NFe']['infNFe']["det"][0]["imposto"]["COFINS"]["COFINSOutr"]["pCOFINS"] = 0
            dict['NFe']['infNFe']["det"][0]["imposto"]["COFINS"]["COFINSOutr"]["vCOFINS"] = 0
            dict['NFe']['infNFe']["det"][0]["imposto"]["PIS"]["PISOutr"]["vBC"] = 0
            dict['NFe']['infNFe']["det"][0]["imposto"]["PIS"]["PISOutr"]["pPIS"] = 0
            dict['NFe']['infNFe']["det"][0]["imposto"]["PIS"]["PISOutr"]["vPIS"] = 0
        complemenatarXML.setXMLDict(dict)

        # 5 - ICMS Total
        dict = complemenatarXML.getXMLDict()
        try:
            dict['NFe']['infNFe']["total"]["ICMSTot"]["vICMS"] = round(float(complemenatarXML.getXMLDict()['NFe']['infNFe']["det"]["imposto"]["ICMS"]["ICMS00"]["vBC"]) * 0.04,2)
        except Exception as e:
            print(e)
            dict['NFe']['infNFe']["total"]["ICMSTot"]["vICMS"] = round(float(complemenatarXML.getXMLDict()['NFe']['infNFe']["det"][0]["imposto"]["ICMS"]["ICMS00"]["vBC"]) * 0.04,2)
        complemenatarXML.setXMLDict(dict)

        # 6 - InfADIC
        dict = complemenatarXML.getXMLDict()

        valores={'data-emissao': originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['dhEmi'],
                 "No_NF": originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['nNF'],
                 "serie": originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['serie']}
        texto=f"""
        Conforme artigo 182 IV do RICMS, Nota fiscal complementar de ICMS
                referente:&lt;br /&gt;A NF {valores["No_NF"]} da serie {valores["serie"]} de {datetime.strptime(valores["data-emissao"].split("T")[0].replace("-","/"),"%Y/%m/%d").strftime("%d/%m/%Y")}.
        """
        dict['NFe']['infNFe']["infAdic"]["infCpl"] = texto

        
        complemenatarXML.setXMLDict(dict)
        #####################################################################################
        print(complemenatarXML.getXMLDict()["NFe"]["infNFe"]["@Id"])
        complemenatarXML.saveXML(os.path.join(targetFolder,complemenatarXML.getXMLDict()['NFe']['infNFe']['@Id']+'.xml'))

if __name__ == '__main__':
    main(sys.argv[1:])