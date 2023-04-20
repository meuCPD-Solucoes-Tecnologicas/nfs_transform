from multiprocessing import Pool
import os
import re
import sys
from pprint import pformat
from nfs_db import nova_nota, select_base
from pyNFS import NFS as nfs
from datetime import datetime
from pynfe_driver import driver as pdriver
from addict import Dict
from pynfe.utils import carregar_arquivo_municipios
from lxml import etree
from progress.bar import Bar


ISO_DATETIME_LOG = f"0_geral_{datetime.now().isoformat()}"


def log(msg, tipo="NORMAL"):
    iso_datetime_registro = datetime.now().isoformat()
    with open(f"log/{ISO_DATETIME_LOG}_{tipo}.log", "a") as fd:
        fd.write(f"{iso_datetime_registro}: {msg}\n")


def gera_complementares(argv):
    """carrega xmls de nfs originais e gera nfs complementares
        - pra cada xml original encontrado, le o arquivo e ignora se o destinatário for de SP
        - salva no banco nNFs.db que incrementa o nNF (PK) e retorna para ser usado com nNF da complementar
        - itera sobre os produtos da original e adiciona na complementar o calculo dos seus icms com base no valor do produto
        - pega o restante das informações necessários (destinatário, endereço, etc) da original e completa a complementar
        - verifica o ambiente
        - carrega a versão dict do xml da complementar
        - chama o metodo de assinatura da pynfe_driver
        - o método retorna um xml (etree.Element) montado (com id, data de emissão, calculos totais, etc) e assinado
        - transforma o xml em string
        - salva o xml string numa pasta
        - salva o xml string no banco nNFs.db
        - append o xml string numa lista
        - retorna a lista de xmls assinados em string para serem enviados
    
    Args:
        argv (list): lista de argumentos
            argv[1]: sourceFolder (pasta de origem)
            argv[2]: targetFolder (pasta de destino)
            argv[3]: templateFolder (pasta de template) 
            usa as flags:
                --envprod e --envio-producao para definir o ambiente de produção
                ----envio-homologacao e --envhom para definir o ambiente de homologação
            
    """
    nextarg = 0

    # pega processo
    arg_numeros = [0, 0]
    args_dest = []
    for arg in argv:
        if arg.startswith("-"):
            args_dest.append(arg)
            nextarg += 1
        try:
            if isinstance(int(arg), int):
                arg_numeros[0 if arg_numeros[0] == 0 else 1] = arg
        except ValueError:
            continue
            # print('arg non int')

    # definição de variaveis pasta de nfs originais e nfs complementares (geradas)
    sourceFolder = os.path.relpath(argv[nextarg])
    targetFolder = os.path.relpath(argv[nextarg + 1])
    templateFOlder = os.path.relpath(argv[nextarg + 2])

    # verifica se a pasta de origem existe
    if not os.path.exists(sourceFolder):
        print("Pasta de origem não encontrada")
        sys.exit(1)

    # verifica se a pasta de destino existe
    if not os.path.exists(targetFolder):
        print("Pasta de destino não encontrada")
        sys.exit(1)

    # verifica se a pasta de template existe
    if not os.path.exists(templateFOlder):
        print("Pasta de template não encontrada")
        sys.exit(1)

    # verifica se a pasta de origem está vazia
    if not os.listdir(sourceFolder):
        print("Pasta de origem vazia")
        sys.exit(1)

    # lista de arquivos xml na pasta de origem
    def sort_por_nome(file_name):
        file_name = file_name.replace("._", "").replace("-nfe", "")
        if re.match(r"[0-9]{44}", file_name) is None:
            raise Exception("Arquivo com nome inválido: " + file_name)
        ano_mes = file_name[2:6]
        nNF = file_name[25:34]
        return ano_mes + nNF

    xmlFiles = sorted(
        [
            f
            for f in os.listdir(sourceFolder)
            if (f.endswith(".xml") and f.split("-")[0])
        ],
        key=sort_por_nome,
    )

    log("Arquivos encontrados e ordenados: " + ",".join(xmlFiles))
    if (
        input(
            "Arquivos encontrados e ordenados: "
            + "\n".join(xmlFiles[:20])
            + f'\n{"...mais "+str((len(xmlFiles)-20)) if len(xmlFiles)>20 else ""} ({len(xmlFiles)} no total)\nContinuar?(s/N)'
        ).lower()
        != "s"
    ):
        exit()

    log("Transformando Complementares:")
    print("Transformando Complementares:")

    # input(
    #     "Números de série encontrados Série 1: "
    #     + str(nNFE_serie_1)
    #     + " Série 2: "
    #     + str(nNFE_serie_2)
    #     + "\nPressione enter para continuar ou ctrl+c para cancelar"
    # )

    ignoradas = 0
    bar = Bar(
        "Processando",
        max=len(xmlFiles),
    )

    xml_assinados = []
    for xmlFile in xmlFiles:
        try:
            originalXML = nfs.XMLPY(
                open(os.path.join(sourceFolder, xmlFile), "r").read()
            )
            log(f"\nAberto Original {os.path.join(sourceFolder, xmlFile)} ")
        except Exception as e:
            log(
                "[ERROR]: erro AO ABRIR ARQUIVO: " + xmlFile + ". Erro: " + str(e),
                tipo="ERROR",
            )
            print("[ERROR]: erro AO ABRIR ARQUIVO: " + xmlFile + ". Erro: " + str(e))
            continue

        if (
            originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"][
                "UF"
            ]
            == "SP"
        ):
            log("[WARNING] " + originalXML.get_chave_de_acesso() + " IGNORADA SP\n")
            ignoradas += 1
            bar.max -= 1
            continue

        valores = {
            "data-emissao": originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["ide"][
                "dhEmi"
            ],
            "No_NF": originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["ide"]["nNF"],
            "serie": originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["ide"][
                "serie"
            ],
        }

        nota_fiscal = nova_nota(
            ambiente="PRODUCAO"
            if ("--envio-producao" in args_dest or "--envprod" in args_dest)
            else "HOMOLOGACAO",
            serie=valores["serie"],
            chave_acesso_nota_original=originalXML.get_chave_de_acesso(),
            nnf_original=valores["No_NF"],
            xml_nota_original=originalXML.getXML(),
        )
        complementarXML = nfs.XMLPY(
            open(os.path.join(templateFOlder, "template.xml"), "r").read()
        )
        log(f"Aberto template {os.path.join(templateFOlder, 'base.xml')}")

        # salva dict original
        # if not os.path.exists("NFS/Dicts_original"):
        #     os.makedirs("NFS/Dicts_original")
        # with open("NFS/Dicts_original/" + xmlFile + ".py", "w+") as fd:
        #     fd.write("nfe_dict=" + pformat(originalXML.getXMLDict()) + "\n")

        # Referencia da complementar na nf original

        # xml_dict = complementarXML.getXMLDict()
        complementarXML.xmldict["NFe"]["infNFe"]["ide"]["NFref"]["refNFe"] = str(
            originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["@Id"]
        ).replace("NFe", "")
        complementarXML.setXMLDict(complementarXML.xmldict)

        # iterando em det (produtos)
        xml_dict_complementar = complementarXML.getXMLDict()

        # Complemento de ICMS
        # save origi(str(complementarXML.getXMLDict())+'\n')

        #### ALTERANDO CAMPOS det #########################################################
        log("Adicionando produtos")

        texto = f'Conforme artigo 182 IV do RICMS, Nota fiscal complementar de ICMS referente a NF {valores["No_NF"]} da serie {str(valores["serie"]).zfill(2)} de {datetime.strptime(valores["data-emissao"].split("T")[0].replace("-","/"),"%Y/%m/%d").strftime("%d/%m/%Y")}.'
        xml_dict_complementar["NFe"]["infNFe"]["infAdic"]["infCpl"] = texto
        xml_dict_complementar["NFe"]["infNFe"]["ide"]["serie"] = valores["serie"]
        xml_dict_complementar["NFe"]["infNFe"]["ide"][
            "natOp"
        ] = f"Complementar de ICMS (Serie {valores['serie']})"

        xml_dict_complementar["NFe"]["infNFe"]["total"]["ICMSTot"]["vBC"] = 0

        nffe_atual_log = (
            "nNFE_atual.log"
            if ("--envio-producao" in args_dest or "--envprod" in args_dest)
            else "nNFE_atual_homolgacao.log"
        )

        if valores["serie"] == "1":
            CFOP_desta_nota = "6108"
            cProd_desta_nota = "CFOP6108"

            complementarXML.getXMLDict()["NFe"]["infNFe"]["ide"][
                "nNF"
            ] = nota_fiscal.nnf_complementar

            with open(nffe_atual_log, "a") as fd:
                fd.write(
                    f"SÉRIE 1: {nota_fiscal.nnf_complementar} nfe original :{nota_fiscal.chave_acesso_nota_original}\n"
                )

            log(
                f"[WARNING] nota original {nota_fiscal.chave_acesso_nota_original} teve sua complementar associada à serie {nota_fiscal.nnf_complementar}"
            )

        elif valores["serie"] == "2":
            CFOP_desta_nota = "6106"
            cProd_desta_nota = "CFOP6106"

            complementarXML.getXMLDict()["NFe"]["infNFe"]["ide"][
                "nNF"
            ] = nota_fiscal.nnf_complementar

            with open(nffe_atual_log, "a") as fd:
                fd.write(
                    f"SÉRIE 2: {nota_fiscal.nnf_complementar} nfe original: {nota_fiscal.chave_acesso_nota_original}\n"
                )

            log(
                f"[WARNING] nota original {originalXML.get_chave_de_acesso()} teve sua complementar associada à serie {nota_fiscal.nnf_complementar}"
            )

        else:
            raise Exception(
                "VALOR DE SÉRIE INVÁLIDO, NÃO INCREMENTANDO E ASSOCIAÇÃO NÃO SALVA. SÉRIE :"
                + valores["serie"]
            )

        temp_list = []
        for produto_original in originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"][
            "det"
        ]:
            produto_atual = Dict(**xml_dict_complementar["NFe"]["infNFe"]["det"][0])

            produto_atual["@nItem"] = produto_original["@nItem"]

            produto_atual.imposto.ICMS.ICMS00.vBC = produto_original["prod"]["vProd"]
            produto_atual.prod.NCM = produto_original["prod"]["NCM"]
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
                round(
                    float(produto_atual["imposto"]["ICMS"]["ICMS00"]["vBC"]) * 0.04, 2
                )
            )

            temp_list.append(produto_atual)
            log("Produto adicionado: " + str(produto_atual))

        xml_dict_complementar["NFe"]["infNFe"]["det"] = temp_list
        log("Produtos adicionados!")

        xml_dict_complementar["NFe"]["infNFe"]["total"]["ICMSTot"]["vICMS"] = "0.00"

        complementarXML.setXMLDict(xml_dict_complementar)
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
        xml_dict_complementar = complementarXML.getXMLDict()
        xml_dict_complementar["NFe"]["infNFe"]["emit"][
            "CNPJ"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"]["CNPJ"]
        xml_dict_complementar["NFe"]["infNFe"]["emit"][
            "xNome"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"]["xNome"]
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["enderEmit"][
            "xLgr"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"][
            "xLgr"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["enderEmit"][
            "nro"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"][
            "nro"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["enderEmit"][
            "xBairro"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"][
            "xBairro"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["enderEmit"][
            "cMun"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"][
            "cMun"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["enderEmit"][
            "xMun"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"][
            "xMun"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["enderEmit"][
            "UF"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"][
            "UF"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["enderEmit"][
            "CEP"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"][
            "CEP"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["enderEmit"][
            "cPais"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"][
            "cPais"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["enderEmit"][
            "xPais"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"][
            "xPais"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["enderEmit"][
            "fone"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"][
            "fone"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["IE"] = originalXML.getXMLDict()[
            "nfeProc"
        ]["NFe"]["infNFe"]["emit"]["IE"]
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["enderEmit"][
            "xCpl"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["emit"][
            "enderEmit"
        ].get(
            "xCpl", ""
        )
        # originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['emit']['CRT']
        xml_dict_complementar["NFe"]["infNFe"]["emit"]["CRT"] = "3"

        complementarXML.setXMLDict(xml_dict_complementar)

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
        xml_dict_complementar = complementarXML.getXMLDict()

        if cpf := originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"].get(
            "CPF"
        ):
            # se cpf existe seta cpf, se não seta cnpj
            xml_dict_complementar["NFe"]["infNFe"]["dest"].update(CPF=cpf)
        else:
            xml_dict_complementar["NFe"]["infNFe"]["dest"].update(
                CNPJ=originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"][
                    "CNPJ"
                ]
            )

        if ie := originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"].get("IE"):
            xml_dict_complementar["NFe"]["infNFe"]["dest"].update(IE=ie)
        #     log("ERRO SCHEMA IE!")

        # # xml_dict['NFe']['infNFe']["dest"]["CPF"] = originalXML.getXMLDict()["nfeProc"]['NFe']['infNFe']['dest']['CPF']
        #
        #     log("keyerro "+str(ke))
        xml_dict_complementar["NFe"]["infNFe"]["dest"][
            "xNome"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"]["xNome"]
        xml_dict_complementar["NFe"]["infNFe"]["dest"]["enderDest"][
            "xLgr"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"][
            "xLgr"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["dest"]["enderDest"][
            "nro"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"][
            "nro"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["dest"]["enderDest"][
            "xBairro"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"][
            "xBairro"
        ]

        xml_dict_complementar["NFe"]["infNFe"]["dest"]["enderDest"][
            "UF"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"][
            "UF"
        ]

        xml_dict_complementar["NFe"]["infNFe"]["dest"]["enderDest"][
            "cMun"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"][
            "cMun"
        ]

        try:
            dict_das_cidades = carregar_arquivo_municipios(
                xml_dict_complementar["NFe"]["infNFe"]["dest"]["enderDest"]["UF"]
            )
            xml_dict_complementar["NFe"]["infNFe"]["dest"]["enderDest"][
                "xMun"
            ] = dict_das_cidades[
                xml_dict_complementar["NFe"]["infNFe"]["dest"]["enderDest"]["cMun"]
            ]
        except KeyError as ke:
            print(
                f"[ERROR][KeyError]: erro em {originalXML.get_chave_de_acesso()}. erro: cMun não encontrado {str(ke)}"
            )
            log(
                f"[ERROR][KeyError]: erro em {originalXML.get_chave_de_acesso()}. erro: cMun não encontrado {str(ke)}",
                tipo="ERROR",
            )
            continue
        except Exception as e:
            __import__("ipdb").set_trace()
            raise

        xml_dict_complementar["NFe"]["infNFe"]["dest"]["enderDest"][
            "CEP"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"][
            "CEP"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["dest"]["enderDest"][
            "cPais"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"][
            "cPais"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["dest"]["enderDest"][
            "xPais"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"][
            "xPais"
        ]
        xml_dict_complementar["NFe"]["infNFe"]["dest"][
            "indIEDest"
        ] = originalXML.getXMLDict()["nfeProc"]["NFe"]["infNFe"]["dest"]["indIEDest"]

        complementarXML.setXMLDict(xml_dict_complementar)

        #####################################################################################
        # print(complementarXML.getXMLDict()["NFe"]["infNFe"]["@Id"])
        arqname = os.path.join(
            targetFolder,
            "COMPLEMENTAR-"
            + complementarXML.getXMLDict()["NFe"]["infNFe"]["ide"]["NFref"]["refNFe"]
            + ".xml",
        )
        complementarXML.saveXML(arqname)
        # open(arqname + ".nfe_dict.py", "w").write(pformat(complementarXML.getXMLDict()))
        log(f"Salvo xml e dict: {arqname}")

        try:
            if "--envio-producao" in args_dest or "--envprod" in args_dest:
                pdriver.configura(
                    caminho_certificado="/home/dev/notas_hell/nfs_transform/NFS/certificados/CERTIFICADO LUZ LED COMERCIO ONLINE_VENCE 13.05.2023.p12",
                    senha_certificado="123456",
                    ambiente_homologacao=False,
                    ignora_producao_warning=True,
                    uf="SP",
                    gera_log=True,
                )

                dicthomo = complementarXML.getXMLDict()

                log("ENVIANDO PARA PRODUÇÃO")
                # Envia a NFe para a SEFAZ HOMOLOGACAO
                xmlassinado = pdriver.converte_para_pynfe_XML_assinado(dicthomo)

                xml_str = etree.tostring(xmlassinado, encoding="unicode")  # type: ignore
                index_id = xml_str.find("Id=") + 7

                id_complementar = (
                    etree.tostring(xmlassinado, encoding="unicode") # type: ignore
                    .split('versao="4.00" Id="')[1]
                    .split("\">")[0]
                )
                log(
                    f"xml assinado: {id_complementar}",
                )
                with open(f"log/{id_complementar}-assinado.xml", "w") as fd:
                    fd.write(xml_str)

                nota_fiscal.xml_nota_complementar = xml_str
                nota_fiscal.chave_acesso_nota_complementar = id_complementar.replace('NFe', '')
                nota_fiscal.save()

                xml_assinados.append(xml_str)
                bar.next()

            elif "--envio-homologacao" in args_dest or "--envhom" in args_dest:
                pdriver.configura(
                    caminho_certificado="/home/dev/notas_hell/nfs_transform/NFS/certificados/CERTIFICADO LUZ LED COMERCIO ONLINE_VENCE 13.05.2023.p12",
                    senha_certificado="123456",
                    ambiente_homologacao=True,
                    uf="SP",
                    gera_log=True,
                )

                dicthomo = complementarXML.getXMLDict()

                # altera xnome para literal "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"
                dicthomo["NFe"]["infNFe"]["dest"][
                    "xNome"
                ] = "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"

                # Envia a NFe para a SEFAZ HOMOLOGACAO
                xmlassinado = pdriver.converte_para_pynfe_XML_assinado(dicthomo)
                xml_str = etree.tostring(xmlassinado, encoding="unicode") # type: ignore

                id_complementar = (
                    etree.tostring(xmlassinado, encoding="unicode") # type: ignore
                    .split('versao="4.00" Id="')[1]
                    .split("\">")[0]
                )
                log(
                    f"xml assinado: {id_complementar}",
                )
                with open(f"log/{id_complementar}-assinado.xml", "w") as fd:
                    fd.write(etree.tostring(xmlassinado, encoding="unicode")) # type: ignore

                nota_fiscal.xml_nota_complementar = xml_str
                nota_fiscal.chave_acesso_nota_complementar = id_complementar.replace('NFe', '')
                nota_fiscal.save()

                xml_assinados.append(xml_str)
                bar.next()

        except Exception as e:
            print(
                f"[ERROR]: erro em {originalXML.get_chave_de_acesso()}. erro: {str(e)}"
            )
            log(
                f"[ERROR]: erro em {originalXML.get_chave_de_acesso()}. erro: {str(e)}",
                tipo="ERROR",
            )
            raise
            continue

    bar.finish()
    print("xml ignoradas: ", ignoradas)
    log("xml ignoradas: " + str(ignoradas))
    return xml_assinados



if __name__ == "__main__":
    xmls = gera_complementares(sys.argv[1:])

    barra_progresso_autorizacao = Bar("Autorizando...", max=len(xmls))
    bar_con = Bar("Consultando...", max=len(xmls))

    input(
        f"{len(xmls)} xmls assinadas, enviar?" + "\nPressione enter para continuar..."
    )

    with Pool(8) as p:
        autorizados = []
        for i in xmls:
            autorizados.append(p.apply_async(pdriver.autorização, [i]))

        consultados = []
        for autorizado in autorizados:
            recibo, tMed, chave_de_acesso = autorizado.get()
            barra_progresso_autorizacao.next()
            
            numero_serie = int(chave_de_acesso[22:25])
            db_base = select_base(ambiente="PRODUCAO" if "--envprod" in sys.argv else "HOMOLOGACAO", serie=numero_serie)
            
            nota = db_base.get(nnf_complementar=chave_de_acesso[25:34])
            nota.enviado_em=datetime.now()
            nota.save()

            consultados.append(
                p.apply_async(
                    pdriver.consulta_recibo,
                    [recibo, chave_de_acesso, tMed],
                )
            )
        barra_progresso_autorizacao.finish()

        for consulta in consultados:
            chave_de_acesso,xml_recibo = consulta.get()

            numero_serie = int(chave_de_acesso[22:25])
            db_base = select_base(ambiente="PRODUCAO" if "--envprod" in sys.argv else "HOMOLOGACAO", serie=numero_serie)
            nota = db_base.get(nnf_complementar=chave_de_acesso[25:34])
            nota.xml__recibo_nota_complementar=xml_recibo
            nota.save()


            bar_con.next()

        bar_con.finish()
