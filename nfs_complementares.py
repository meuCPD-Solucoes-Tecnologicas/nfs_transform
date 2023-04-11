
import os
import sys
from pprint import pformat
from time import sleep
from pyNFS import NFS as nfs
from datetime import datetime
from pytz import timezone
from pynfe_driver import pynfe_driver as pdriver
from decimal import Decimal
from addict import Dict


def main(argv):

    nextarg = 0

    # pega processo
    arg_numeros = [0, 0]
    args_dest = []
    for arg in argv:
        if (arg.startswith("-")):
            args_dest.append(arg)
            nextarg += 1
        try:
            if (isinstance(int(arg), int)):
                arg_numeros[0 if arg_numeros[0] == 0 else 1] = arg
        except ValueError:
            print('arg non int')

    # definição de variaveis pasta de nfs originais e nfs complementares (geradas)
    sourceFolder = os.path.relpath(argv[nextarg])
    targetFolder = os.path.relpath(argv[nextarg+1])
    baseFOlder = os.path.relpath(argv[nextarg+2])

    # verifica se a pasta de origem existe
    if not os.path.exists(sourceFolder):
        print("Pasta de origem não encontrada")
        sys.exit(1)

    # verifica se a pasta de destino existe
    if not os.path.exists(targetFolder):
        print("Pasta de destino não encontrada")
        sys.exit(1)

    # verifica se a pasta de base existe
    if not os.path.exists(baseFOlder):
        print("Pasta de base não encontrada")
        sys.exit(1)

    # verifica se a pasta de origem está vazia
    if not os.listdir(sourceFolder):
        print("Pasta de origem vazia")
        sys.exit(1)

    # lista de arquivos xml na pasta de origem
    xmlFiles = [f for f in os.listdir(sourceFolder) if f.endswith('.xml')]
    print("Arquivos Encontrados:")
    for xmlfile in xmlFiles:
        print(xmlfile)

    print("Transformando Complementares:")
    nNFE_serie_1 = int(arg_numeros[0])
    nNFE_serie_2 = int(arg_numeros[1])
    # if not nNFE_serie_1
    for xmlFile in xmlFiles:

        originalXML = nfs.XMLPY(
            open(os.path.join(sourceFolder, xmlFile), 'r').read())

        # if (originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']["ide"]['cUF']):
        #     continue

        complementarXML = nfs.XMLPY(
            open(os.path.join(baseFOlder, "base.xml"), 'r').read())
        #####################################################################################
        # salva dict original
        if not os.path.exists("NFS/Dicts_original"):
            os.makedirs("NFS/Dicts_original")
        with open("NFS/Dicts_original/"+xmlFile+".py", 'w+') as fd:
            fd.write("nfe_dict="+pformat(originalXML.getXMLDict())+'\n')

        # Referencia da complementar na nf original

        # xml_dict = complementarXML.getXMLDict()
        complementarXML.xmldict["NFe"]["infNFe"]["ide"]["NFref"]["refNFe"] = str(
            originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']["@Id"]).replace("NFe", "")
        complementarXML.setXMLDict(complementarXML.xmldict)

        # nNF da complementar
        # começa em 2708 com 6 digitos e vai incrementando
        xml_dict = complementarXML.getXMLDict()

        complementarXML.setXMLDict(xml_dict)

        # definir data de emissão da complementar
        # Definir o fuso horário
        tz = timezone('America/Sao_Paulo')

        # Obter a data e hora atual no fuso horário especificado
        now = datetime.now(tz)

        # Formatar a data e hora no formato desejado como o exemplo abaixo
        # 2023-03-21T16:19:49-03:00
        formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S-03:00")

        xml_dict = complementarXML.getXMLDict()
        complementarXML.getXMLDict(
        )["NFe"]["infNFe"]["ide"]["dhEmi"] = formatted_date
        complementarXML.setXMLDict(xml_dict)

        # cNF e cDV da complementar

        xml_dict = complementarXML.getXMLDict()
        complementarXML.getXMLDict()["NFe"]["infNFe"]["ide"]["cNF"] = originalXML.getXMLDict()[
            "nfeProc"]['NFe']['infNFe']['ide']['cNF']

        # iterando em det
        xml_dict = complementarXML.getXMLDict()

        # Complemento de ICMS
        # save original value on file
        with open(os.path.join(targetFolder, "originalvalue.py"), 'w+') as fd:
            fd.write(str(complementarXML.getXMLDict())+'\n')

        #### ALTERANDO CAMPOS det #########################################################

        valores = {'data-emissao': originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['dhEmi'],
                   "No_NF": originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['nNF'],
                   "serie": originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['serie']}
        texto = f"""Conforme artigo 182 IV do RICMS, Nota fiscal complementar de ICMS referente a NF {valores["No_NF"]} da serie {str(valores["serie"]).zfill(2)} de {datetime.strptime(valores["data-emissao"].split("T")[0].replace("-","/"),"%Y/%m/%d").strftime("%d/%m/%Y")}."""
        xml_dict['NFe']['infNFe']["infAdic"]["infCpl"] = texto
        xml_dict['NFe']['infNFe']["ide"]["serie"] = valores['serie']
        xml_dict['NFe']['infNFe']["ide"][
            "natOp"] = f"Complementar de ICMS (Serie {valores['serie']})"

        xml_dict['NFe']['infNFe']['total']['ICMSTot']['vBC'] = 0

        temp_list = []
        for produto_original in originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det']:
            produto_atual = Dict(**xml_dict['NFe']['infNFe']['det'][0])

            produto_atual['@nItem'] = produto_original['@nItem']

            produto_atual.imposto.ICMS.ICMS00.vBC = produto_original['prod']['vProd']
            produto_atual.prod.NCM = produto_original['prod']['NCM']
            produto_atual.prod.qCom = 1.0000

            # ????? / TODO
            # xml_dict['NFe']['infNFe']['total']['ICMSTot']['vBC'] = originalXML.getXMLDict(
            # )['nfeProc']['NFe']['infNFe']['det'][0]['prod']['vProd']

            # novo_vbc = Decimal(xml_dict['NFe']['infNFe']['total']
            #                    ['ICMSTot']['vBC']) + Decimal(o_det['prod']['vProd'])
            # novo_vbc = Decimal(o_det['prod']['vProd'])
            # xml_dict['NFe']['infNFe']['total']['ICMSTot']['vBC'] = "{:.2f}".format(
            #     novo_vbc)

            #  Complemento de CONFINS
            produto_atual.imposto.COFINS.COFINSOutr.vBC = str("0.00")
            produto_atual.imposto.COFINS.COFINSOutr.pCOFINS = str("0.00")
            produto_atual.imposto.COFINS.COFINSOutr.vCOFINS = str("0.00")
            produto_atual.imposto.PIS.PISOutr.vBC = str("0.00")
            produto_atual.imposto.PIS.PISOutr.pPIS = str("0.00")
            produto_atual.imposto.PIS.PISOutr.vPIS = str("0.00")

            # ICMS Total
            produto_atual["imposto"]["ICMS"]["ICMS00"]["vICMS"] = "{:.2f}".format(
                round(float(produto_atual["imposto"]["ICMS"]["ICMS00"]["vBC"]) * 0.04, 2))

            if (valores['serie'] == '1'):
                produto_atual.prod.CFOP = '6108'
                produto_atual.prod.cProd = 'CFOP6108'
                complementarXML.getXMLDict(
                )["NFe"]["infNFe"]["ide"]["nNF"] = str(nNFE_serie_1)
                with open('nNFE_atual', 'a') as fd:
                    fd.write("\nnNFE_serie_1: "+str(nNFE_serie_1))
                nNFE_serie_1 += 1

            elif (valores['serie'] == '2'):
                produto_atual.prod.CFOP = '6106'
                produto_atual.prod.cProd = 'CFOP6106'
                complementarXML.getXMLDict(
                )["NFe"]["infNFe"]["ide"]["nNF"] = str(nNFE_serie_2)
                with open('nNFE_atual', 'a') as fd:
                    fd.write("\nnNFE_serie_2: "+str(nNFE_serie_2))
                nNFE_serie_2 += 1

            temp_list.append(produto_atual)

        xml_dict['NFe']['infNFe']['det'] = temp_list

        xml_dict['NFe']['infNFe']['total']['ICMSTot']['vICMS'] = '0.00'

        complementarXML.setXMLDict(xml_dict)
        ############################################################################################

        # emit

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
        xml_dict = complementarXML.getXMLDict()
        xml_dict['NFe']['infNFe']["emit"]["CNPJ"] = originalXML.getXMLDict()[
            "nfeProc"]['NFe']['infNFe']['emit']['CNPJ']
        xml_dict['NFe']['infNFe']["emit"]["xNome"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['emit']['xNome']
        xml_dict['NFe']['infNFe']["emit"]["enderEmit"]["xLgr"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['xLgr']
        xml_dict['NFe']['infNFe']["emit"]["enderEmit"]["nro"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['nro']
        xml_dict['NFe']['infNFe']["emit"]["enderEmit"]["xBairro"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['xBairro']
        xml_dict['NFe']['infNFe']["emit"]["enderEmit"]["cMun"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['cMun']
        xml_dict['NFe']['infNFe']["emit"]["enderEmit"]["xMun"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['xMun']
        xml_dict['NFe']['infNFe']["emit"]["enderEmit"]["UF"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['UF']
        xml_dict['NFe']['infNFe']["emit"]["enderEmit"]["CEP"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['CEP']
        xml_dict['NFe']['infNFe']["emit"]["enderEmit"]["cPais"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['cPais']
        xml_dict['NFe']['infNFe']["emit"]["enderEmit"]["xPais"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['xPais']
        xml_dict['NFe']['infNFe']["emit"]["enderEmit"]["fone"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['emit']['enderEmit']['fone']
        xml_dict['NFe']['infNFe']["emit"]["IE"] = originalXML.getXMLDict()[
            "nfeProc"]['NFe']['infNFe']['emit']['IE']
        xml_dict['NFe']['infNFe']["emit"]["enderEmit"]['xCpl'] = originalXML.getXMLDict()[
            "nfeProc"]['NFe']['infNFe']['emit']["enderEmit"]['xCpl']
        # originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['CRT']
        xml_dict['NFe']['infNFe']["emit"]["CRT"] = '3'

        complementarXML.setXMLDict(xml_dict)

        # dest
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
        xml_dict = complementarXML.getXMLDict()

        xml_dict['NFe']['infNFe']["dest"]["CPF"] = originalXML.getXMLDict()[
            "nfeProc"]['NFe']['infNFe']['dest']['CPF']
        xml_dict['NFe']['infNFe']["dest"]["xNome"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['xNome']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["xLgr"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['xLgr']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["nro"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['nro']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["xBairro"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['xBairro']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["cMun"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['cMun']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["xMun"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['xMun']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["UF"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['UF']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["CEP"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['CEP']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["cPais"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['cPais']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["xPais"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['xPais']
        xml_dict['NFe']['infNFe']["dest"]["indIEDest"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['indIEDest']

        complementarXML.setXMLDict(xml_dict)

        # gerar o id da nota
        # xml_dict = complementarXML.getXMLDict()
        # complementarXML.generate_NFeID()
        # xml_dict["NFe"]["infNFe"]["@Id"] = complementarXML.id
        # complementarXML.setXMLDict(xml_dict)
        # # Assinar o XML
        # complementarXML.setXML(complementarXML.sign_procNfe("./NFS/certificados/CERTIFICADO_LUZ_LED_COMERCIO_ONLINE_VENCE_13.05.2023.p12","123456"))

        #####################################################################################
        print(complementarXML.getXMLDict()["NFe"]["infNFe"]["@Id"])
        arqname = os.path.join(targetFolder, "COMPLEMENTAR-"+complementarXML.getXMLDict()[
                               "NFe"]["infNFe"]["ide"]["NFref"]["refNFe"]+'.xml')
        complementarXML.saveXML(arqname)
        open(arqname+'.nfe_dict.py',
             'w').write(pformat(complementarXML.getXMLDict()))
        # processo de envio

        if ("--envio-producao" in args_dest or "--envprod" in args_dest):
            pdriver.configura(
                caminho_certificado="./NFS/certificados/CERTIFICADO_LUZ_LED_COMERCIO_ONLINE_VENCE_13.05.2023.p12",
                senha_certificado="123456",
                ambiente_homologacao=False,
                uf="SP",
                gera_log=True
            )

            pdriver._teste_configurado()  # Verifica se o ambiente está configurado corretamente

            dicthomo = complementarXML.getXMLDict()

            # altera xnome para literal "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"
            dicthomo["NFe"]["infNFe"]["dest"]["xNome"] = "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"

            # Envia a NFe para a SEFAZ HOMOLOGACAO
            xmlassinado = pdriver.converte_para_pynfe_XML_assinado(dicthomo)
            chaveretornada = pdriver.autorização(xmlassinado)

            pdriver.consulta_recibo(chaveretornada)

        if ("--envio-homologacao" in args_dest or "--envhom" in args_dest):
            pdriver.configura(
                caminho_certificado="/home/dev/nfs_transform/NFS/certificados/CERTIFICADO LUZ LED COMERCIO ONLINE_VENCE 13.05.2023.p12",
                senha_certificado="123456",
                ambiente_homologacao=True,
                uf="SP",
                gera_log=True
            )

            pdriver._teste_configurado()  # Verifica se o ambiente está configurado corretamente

            dicthomo = complementarXML.getXMLDict()
            with open("braba"".py", 'w+') as fd:
                fd.write("nfe_dict="+pformat(complementarXML.getXMLDict())+'\n')

            # altera xnome para literal "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"
            dicthomo["NFe"]["infNFe"]["dest"]["xNome"] = "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"

            # Envia a NFe para a SEFAZ HOMOLOGACAO
            xmlassinado = pdriver.converte_para_pynfe_XML_assinado(dicthomo)
            chaveretornada = pdriver.autorização(xmlassinado)

            sleep(3)

            pdriver.consulta_recibo(chaveretornada)


if __name__ == '__main__':
    main(sys.argv[1:])
