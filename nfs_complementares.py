from multiprocessing import Pool
import os
import re
import sys
from pprint import pformat
from pyNFS import NFS as nfs
from datetime import datetime
from pytz import timezone
from pynfe_driver import pynfe_driver as pdriver
from addict import Dict
from pynfe.utils import carregar_arquivo_municipios
from lxml import etree
from progress.bar import Bar


now_log = f'0_geral_{datetime.now().isoformat()}'


def log(msg='', tipo='NORMAL'):
    now = datetime.now().isoformat()
    with open(f'log/{now_log}_{tipo}.log', 'a') as fd:
        fd.write(f'{now}: {msg}\n')


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
            continue
            # print('arg non int')

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
    def sort_por_nome(file_name):
        file_name = file_name.replace("._", "").replace("-nfe", "")
        if re.match(r'[0-9]{44}', file_name) is None:
            raise Exception("Arquivo com nome inválido: "+file_name)
        ano_mes = file_name[2:6]
        nNF = file_name[25:34]
        return ano_mes+nNF
    
    xmlFiles: list
    with open("notas_nao_enviadas.txt", "r") as fd:
        notas_nao_enviadas = fd.read()
        xmlFiles = sorted(
            [
                f
                for f in os.listdir(sourceFolder)
                if (
                    # '35221046364058000115550020000060791887089730-nfe.xml'
                    f.endswith(".xml")
                    and not f.split("-")[0] in notas_nao_enviadas
                )
            ],
            key=sort_por_nome,
        )
    # assert (
    #     len(xmlFiles) == 906
    # ), "Número de notas não enviadas diferente do esperado" + str(len(xmlFiles))
    # xmlFiles = xmlFiles[0:1650]
    # xmlFiles = xmlFiles[1650:1650*2]
    # xmlFiles = xmlFiles[1650*2:1650*3]

    log(
        "Arquivos encontrados e ordenados: "+','.join(xmlFiles)
    )
    if (
        input(
            "Arquivos encontrados e ordenados: "+'\n'.join(
            xmlFiles[:20])+ f'\n{"...mais "+str((len(xmlFiles)-20)) if len(xmlFiles)>20 else ""} ({len(xmlFiles)} no total)\nContinuar?(s/N)'
            ).lower() != 's'
        # ).lower() != 's'
    ):
        exit()

    log("Transformando Complementares:")
    print("Transformando Complementares:")

    nNFE_serie_1 = int(arg_numeros[0])
    nNFE_serie_2 = int(arg_numeros[1])

    input("Números de série encontrados Série 1: "+str(nNFE_serie_1) +
          " Série 2: "+str(nNFE_serie_2)+"\nPressione enter para continuar ou ctrl+c para cancelar")

    ignoradas = 0
    len_xmlFiles = len(xmlFiles)
    bar = Bar("Processando", max=len_xmlFiles,
            #   fill="☭"
              )
    bar.max
    xml_assinados = []
    for xmlFile in xmlFiles:
        try:
            originalXML = nfs.XMLPY(
                open(os.path.join(sourceFolder, xmlFile), 'r').read())
            log(f"\nAberto Original {os.path.join(sourceFolder, xmlFile)} ")
        except Exception as e:
            log("[ERROR]: erro AO ABRIR ARQUIVO: " +
                xmlFile+". Erro: "+str(e),
                tipo="ERROR"
                )
            print("[ERROR]: erro AO ABRIR ARQUIVO: " +
                  xmlFile+". Erro: "+str(e))
            continue

        if originalXML.getXMLDict()['nfeProc']['NFe']['infNFe']['dest']['enderDest']['UF'] == 'SP':
            log('[WARNING] ' + originalXML.get_chave_de_acesso()+' IGNORADA SP\n')
            ignoradas+=1
            len_xmlFiles-=1
            continue

        complementarXML = nfs.XMLPY(
            open(os.path.join(baseFOlder, "base.xml"), 'r').read())
        log(f"Aberto template {os.path.join(baseFOlder, 'base.xml')}")

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
        # save origi(str(complementarXML.getXMLDict())+'\n')

        #### ALTERANDO CAMPOS det #########################################################
        log("Adicionando produtos")
        valores = {'data-emissao': originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['dhEmi'],
                   "No_NF": originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['nNF'],
                   "serie": originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['ide']['serie']}
        texto = f"""Conforme artigo 182 IV do RICMS, Nota fiscal complementar de ICMS referente a NF {valores["No_NF"]} da serie {str(valores["serie"]).zfill(2)} de {datetime.strptime(valores["data-emissao"].split("T")[0].replace("-","/"),"%Y/%m/%d").strftime("%d/%m/%Y")}."""
        xml_dict['NFe']['infNFe']["infAdic"]["infCpl"] = texto
        xml_dict['NFe']['infNFe']["ide"]["serie"] = valores['serie']
        xml_dict['NFe']['infNFe']["ide"][
            "natOp"] = f"Complementar de ICMS (Serie {valores['serie']})"

        xml_dict['NFe']['infNFe']['total']['ICMSTot']['vBC'] = 0


        nffe_atual_log = (
            "nNFE_atual.log"
            if ("--envio-producao" in args_dest or "--envprod" in args_dest)
            else "nNFE_atual_homolgacao.log"
        )

        if (valores['serie'] == '1'):
            CFOP_desta_nota = '6108'
            cProd_desta_nota = 'CFOP6108'

            complementarXML.getXMLDict(
            )["NFe"]["infNFe"]["ide"]["nNF"] = str(nNFE_serie_1)

            with open(nffe_atual_log, 'a') as fd:
                fd.write("SÉRIE 1: "+str(nNFE_serie_1) +
                         ' nfe original:'+originalXML.get_chave_de_acesso()+' []'+'\n')

            log(f"[WARNING] nota original {originalXML.get_chave_de_acesso()} teve sua complementar associada à serie {nNFE_serie_1}")

            nNFE_serie_1 += 1

        elif (valores['serie'] == '2'):
            CFOP_desta_nota = '6106'
            cProd_desta_nota = 'CFOP6106'

            complementarXML.getXMLDict(
            )["NFe"]["infNFe"]["ide"]["nNF"] = str(nNFE_serie_2)

            with open(nffe_atual_log, 'a') as fd:
                fd.write("SÉRIE 2: "+str(nNFE_serie_2) +
                         ' nfe original:'+originalXML.get_chave_de_acesso()+' []'+'\n')

            log(f"[WARNING] nota original {originalXML.get_chave_de_acesso()} teve sua complementar associada à serie {nNFE_serie_2}")
            nNFE_serie_2 += 1

        else:
            raise Exception(
                "VALOR DE SÉRIE INVÁLIDO, NÃO INCREMENTANDO E ASSOCIAÇÃO NÃO SALVA. SÉRIE :" + valores['serie'])

        temp_list = []
        for produto_original in originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['det']:
            produto_atual = Dict(**xml_dict['NFe']['infNFe']['det'][0])

            produto_atual['@nItem'] = produto_original['@nItem']

            produto_atual.imposto.ICMS.ICMS00.vBC = produto_original['prod']['vProd']
            produto_atual.prod.NCM = produto_original['prod']['NCM']
            produto_atual.prod.qCom = 1.0000

            produto_atual.prod.CFOP = CFOP_desta_nota
            produto_atual.prod.cProd = cProd_desta_nota

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

            temp_list.append(produto_atual)
            log("Produto adicionado: "+str(produto_atual))

        xml_dict['NFe']['infNFe']['det'] = temp_list
        log("Produtos adicionados!")

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
            "nfeProc"]['NFe']['infNFe']['emit']["enderEmit"].get('xCpl', '')
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

        if (
            cpf := originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest'].get('CPF')
        ):
            # se cpf existe seta cpf, se não seta cnpj
            xml_dict['NFe']['infNFe']["dest"].update(CPF=cpf)
        else:
            xml_dict['NFe']['infNFe']["dest"].update(CNPJ=originalXML.getXMLDict()[
                                                     "nfeProc"]['NFe']['infNFe']['dest']['CNPJ'])

        if (
            ie := originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest'].get('IE')
        ):
            xml_dict['NFe']['infNFe']["dest"].update(IE=ie)
        #     log("ERRO SCHEMA IE!")

        # # xml_dict['NFe']['infNFe']["dest"]["CPF"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['CPF']
        #
        #     log("keyerro "+str(ke))
        xml_dict['NFe']['infNFe']["dest"]["xNome"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['xNome']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["xLgr"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['xLgr']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["nro"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['nro']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["xBairro"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['xBairro']

        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["UF"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['UF']

        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["cMun"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['cMun']

        try:
            dict_das_cidades = carregar_arquivo_municipios(
                xml_dict['NFe']['infNFe']["dest"]["enderDest"]["UF"])
            xml_dict['NFe']['infNFe']["dest"]["enderDest"]["xMun"] = dict_das_cidades[xml_dict['NFe']
                                                                                    ['infNFe']["dest"]["enderDest"]['cMun']]
        except KeyError as ke:
            print(
                f'[ERROR][KeyError]: erro em {originalXML.get_chave_de_acesso()}. erro: cMun não encontrado {str(ke)}')
            log(f'[ERROR][KeyError]: erro em {originalXML.get_chave_de_acesso()}. erro: cMun não encontrado {str(ke)}',
                tipo="ERROR")
            continue
        except Exception as e:
            __import__('ipdb').set_trace()
            raise

        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["CEP"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['CEP']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["cPais"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['cPais']
        xml_dict['NFe']['infNFe']["dest"]["enderDest"]["xPais"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['enderDest']['xPais']
        xml_dict['NFe']['infNFe']["dest"]["indIEDest"] = originalXML.getXMLDict(
        )["nfeProc"]['NFe']['infNFe']['dest']['indIEDest']

        complementarXML.setXMLDict(xml_dict)


        #####################################################################################
        # print(complementarXML.getXMLDict()["NFe"]["infNFe"]["@Id"])
        arqname = os.path.join(targetFolder, "COMPLEMENTAR-"+complementarXML.getXMLDict()[
                               "NFe"]["infNFe"]["ide"]["NFref"]["refNFe"]+'.xml')
        complementarXML.saveXML(arqname)
        open(arqname+'.nfe_dict.py',
             'w').write(pformat(complementarXML.getXMLDict()))
        log(f"Salvo xml e dict: {arqname}")

        try:
            if ("--envio-producao" in args_dest or "--envprod" in args_dest):
                pdriver.configura(
                    caminho_certificado="/home/dev/notas_hell/nfs_transform/NFS/certificados/CERTIFICADO LUZ LED COMERCIO ONLINE_VENCE 13.05.2023.p12",
                    senha_certificado="123456",
                    ambiente_homologacao=False,
                    ignora_producao_warning=True,
                    uf="SP",
                    gera_log=True
                )

                dicthomo = complementarXML.getXMLDict()

                log("ENVIANDO PARA PRODUÇÃO")
                # Envia a NFe para a SEFAZ HOMOLOGACAO
                xmlassinado = pdriver.converte_para_pynfe_XML_assinado(dicthomo)

                xml_str = etree.tostring(xmlassinado, encoding="unicode")
                index_id = xml_str.find("Id=") + 7

                xmlassinado = pdriver.converte_para_pynfe_XML_assinado(dicthomo)
                id_complementar = (
                    etree.tostring(xmlassinado, encoding="unicode")
                    .split('versao="4.00" Id="')[1]
                    .split(">")[0]
                )
                log(
                    f"xml assinado: {id_complementar}",
                )
                with open(f"log/{id_complementar}-assinado.xml", "w") as fd:
                    fd.write(etree.tostring(xmlassinado, encoding="unicode"))

                xml_assinados.append(xmlassinado)
                bar.next()

                # def consulta_com_sleep(recibo, tMed, chave_de_acesso):
                #     sleep(tMed)
                #     pdriver.consulta_recibo(recibo, chave_de_acesso)

                # def autoriza_process(xmlassinado):

                #     try:

                #         recibo, tMed,chave_de_acesso = pdriver.autorização(xmlassinado)
                #     except Exception as e:
                #         log(f'[ERROR]: erro em autorização da complementar {originalXML.get_chave_de_acesso()}. erro: {str(e)}',
                #             tipo="ERROR")
                #         raise
                #     else:
                #         ...
                #         #     fd.write()
                #         # with open("nNFE_atual_sucesso.log", 'a') as fd:
                #         #     arquivo = arquivo.replace(
                #         #         originalXML.get_chave_de_acesso() + ' []', originalXML.get_chave_de_acesso()+' [OK]')
                #         #     fd.seek(0)
                #         #     fd.write(arquivo)

                #     tMed += 5

                #     Process(
                #         name='consulta_nfes',
                #         target=consulta_com_sleep,
                #         args=(recibo, tMed, chave_de_acesso),
                #         # daemon=True
                #     ).start()
                # Process(
                #     name='autoriza_nfes',
                #     target=autoriza_process,
                #     args=(xmlassinado,),
                #     # daemon=True
                # ).start()

            elif ("--envio-homologacao" in args_dest or "--envhom" in args_dest):
                pdriver.configura(
                    caminho_certificado="/home/dev/notas_hell/nfs_transform/NFS/certificados/CERTIFICADO LUZ LED COMERCIO ONLINE_VENCE 13.05.2023.p12",
                    senha_certificado="123456",
                    ambiente_homologacao=True,
                    uf="SP",
                    gera_log=True
                )

                dicthomo = complementarXML.getXMLDict()

                # altera xnome para literal "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"
                dicthomo["NFe"]["infNFe"]["dest"]["xNome"] = "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"

                # Envia a NFe para a SEFAZ HOMOLOGACAO
                xmlassinado = pdriver.converte_para_pynfe_XML_assinado(
                    dicthomo)
                
                id_complementar = (
                    etree.tostring(xmlassinado, encoding="unicode")
                    .split('versao="4.00" Id="')[1]
                    .split(">")[0]
                )
                log(
                    f"xml assinado: {id_complementar}",
                )
                with open(f"log/{id_complementar}-assinado.xml", "w") as fd:
                    fd.write(etree.tostring(xmlassinado, encoding="unicode"))

                xml_assinados.append(xmlassinado)
                bar.next()
                
                # def consulta_com_sleep(recibo, tMed,chave_de_acesso):
                #     sleep(tMed)
                #     pdriver.consulta_recibo(recibo,chave_de_acesso)

                # def autoriza_process(xmlassinado):

                #     try:

                #         recibo, tMed,chave_de_acesso = pdriver.autorização(xmlassinado)
                #     except Exception as e:
                #         log(f'[ERROR]: erro em autorização da complementar {originalXML.get_chave_de_acesso()}. erro: {str(e)}',
                #             tipo="ERROR")
                #         raise
                #     else:
                #         ...
                #         # with open("nNFE_atual_sucesso.log", 'a') as fd:
                #         #     fd.write()

                        
                #     tMed += 15

                #     Process(
                #         name='consulta_nfes',
                #         target=consulta_com_sleep,
                #         args=(recibo, tMed,chave_de_acesso),
                #         # daemon=True
                #     ).start()
                # Process(
                #     name='autoriza_nfes',
                #     target=autoriza_process,
                #     args=(xmlassinado,),
                #     # daemon=True
                # ).start()
                # # autoriza_process(xmlassinado)
        except Exception as e:
            print(
                f'[ERROR]: erro em {originalXML.get_chave_de_acesso()}. erro: {str(e)}')
            log(f'[ERROR]: erro em {originalXML.get_chave_de_acesso()}. erro: {str(e)}',
                tipo="ERROR")
            continue


    bar.finish()
    print("xml ignoradas: ", ignoradas)
    log("xml ignoradas: ", ignoradas)
    return xml_assinados


from lxml import etree
if __name__ == "__main__":

    xmls = main(sys.argv[1:])

    bar = Bar("Autorizando...", max=len(xmls),fill="☭")
    bar_con = Bar("Consultando...", max=len(xmls),fill="☭")

    input(f"{len(xmls)} xmls assinadas, enviar?"+"\nPressione enter para continuar...")

    with Pool(8) as p:
        autorizados = []
        for i in xmls:
            autorizados.append(
                p.apply_async(pdriver.autorização, [etree.tostring(i)])
                )
        
        consultados = []
        for autorizado in autorizados:
            recibo, tMed, chave_de_acesso = autorizado.get()
            bar.next()
            consultados.append(
                p.apply_async(pdriver.consulta_recibo, [recibo, chave_de_acesso,tMed],)
            )
        bar.finish()
        [(i.get(),bar_con.next()) for i in consultados]        
        bar_con.finish()
    

