from datetime import datetime
from decimal import Decimal

try:
    from .mapa_variaveis_Pynfe_X_campos_NFe import mapCliente, mapEmitente, mapProduto, mapaT
except ImportError:
    from pynfe_driver.mapa_variaveis_Pynfe_X_campos_NFe import mapCliente, mapEmitente, mapProduto, mapaT

from pynfe.entidades.fonte_dados import _fonte_dados
from pynfe.entidades.notafiscal import NotaFiscal
from pynfe.entidades import Emitente,Cliente,EventoCancelarNota
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.utils.flags import CODIGOS_ESTADOS
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoSefaz
from lxml import etree
import os

import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) # type: ignore

HOMOLOGACAO: bool
CERTIFICADO: str
SENHA_CERTIFICADO: str
UF = "SP"
CODIGOS_ESTADOS_T = {v: k for k, v in CODIGOS_ESTADOS.items()}
PASTA_LOG = "log"
IGNORA_PRODUCAO_WARNING: bool
DATETIME: str

con: ComunicacaoSefaz
GERA_LOG: bool


def configura(
    caminho_certificado: str,
    senha_certificado: str,
    ambiente_homologacao=True,
    uf="SP",
    gera_log=True,
    ignora_producao_warning=False,
):
    global HOMOLOGACAO
    global con
    global GERA_LOG
    global IGNORA_PRODUCAO_WARNING
    global CERTIFICADO
    global SENHA_CERTIFICADO
    global DATETIME


    # os file exists
    if not os.path.exists(caminho_certificado):
        raise Exception("Certificado não encontrado\n" + caminho_certificado)

    CERTIFICADO = caminho_certificado
    SENHA_CERTIFICADO = senha_certificado

    IGNORA_PRODUCAO_WARNING = ignora_producao_warning
    GERA_LOG = gera_log
    con = ComunicacaoSefaz(
        uf, caminho_certificado, senha_certificado, ambiente_homologacao
    )
    HOMOLOGACAO = ambiente_homologacao
    DATETIME = datetime.now().isoformat()
    # return


def _teste_configurado():
    if HOMOLOGACAO is None:
        raise Exception("HOMOLOGACAO não configurados")
    if con is None:
        raise Exception("con não configurados")
    if GERA_LOG is None:
        raise Exception("log não configurados")
    if IGNORA_PRODUCAO_WARNING is None:
        raise Exception("IGNORA_HOMOLOGACAO_WARNING não configurados")


def converte_para_pynfe_XML_assinado(nfe_dict: dict):
    _teste_configurado()

    try:
        nfe_dict = nfe_dict["nfeProc"]["NFe"]["infNFe"]
    except:
        nfe_dict = nfe_dict["NFe"]["infNFe"]

    nfe_emit: dict = nfe_dict["emit"]

    _emitente = dict(
        cnae_fiscal=nfe_emit.get(mapEmitente("cnae_fiscal")),
        cnpj=nfe_emit.get(mapEmitente("cnpj")),
        codigo_de_regime_tributario=nfe_emit.get(
            mapEmitente("codigo_de_regime_tributario")
        ),
        endereco_bairro=nfe_emit.get("enderEmit", {}).get(
            mapEmitente("endereco_bairro")
        ),
        endereco_cep=nfe_emit.get("enderEmit", {}).get(mapEmitente("endereco_cep")),
        endereco_cod_municipio=nfe_emit.get("enderEmit", {}).get(
            mapEmitente("endereco_cod_municipio")
        ),
        endereco_complemento=nfe_emit.get("enderEmit", {}).get(
            mapEmitente("endereco_complemento")
        ),
        endereco_logradouro=nfe_emit.get("enderEmit", {}).get(
            mapEmitente("endereco_logradouro")
        ),
        endereco_municipio=nfe_emit.get("enderEmit", {}).get(
            mapEmitente("endereco_municipio")
        ),
        endereco_numero=nfe_emit.get("enderEmit", {}).get(
            mapEmitente("endereco_numero")
        ),
        endereco_pais=nfe_emit.get("enderEmit", {}).get(mapEmitente("endereco_pais")),
        endereco_telefone=nfe_emit.get("enderEmit", {}).get(
            mapEmitente("endereco_telefone")
        ),
        endereco_uf=nfe_emit.get("enderEmit", {}).get(mapEmitente("endereco_uf")),
        inscricao_estadual=nfe_emit.get(mapEmitente("inscricao_estadual")),
        inscricao_estadual_subst_tributaria=nfe_emit.get(
            mapEmitente("inscricao_estadual_subst_tributaria")
        ),
        inscricao_municipal=nfe_emit.get(mapEmitente("inscricao_municipal")),
        nome_fantasia=nfe_emit.get(mapEmitente("nome_fantasia")),
        razao_social=nfe_emit.get(mapEmitente("razao_social")),
    )

    nfe_cliente: dict = nfe_dict["dest"]
    _cliente = dict(
        email=nfe_cliente.get(mapCliente("email"), ""),
        endereco_bairro=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_bairro"), ""
        ),
        endereco_cep=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_cep"), ""
        ),
        endereco_cod_municipio=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_cod_municipio"), ""
        ),
        endereco_complemento=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_complemento"), ""
        ),
        endereco_logradouro=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_logradouro"), ""
        ),
        endereco_municipio=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_municipio"), ""
        ),
        endereco_numero=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_numero"), ""
        ),
        endereco_pais=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_pais"), ""
        ),
        endereco_telefone=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_telefone"), ""
        ),
        endereco_uf=nfe_cliente.get("enderDest", {}).get(mapCliente("endereco_uf"), ""),
        indicador_ie=int(nfe_cliente.get(mapCliente("indicador_ie"), "")),
        inscricao_estadual=nfe_cliente.get(mapCliente("inscricao_estadual")),
        inscricao_municipal=nfe_cliente.get(mapCliente("inscricao_municipal"), ""),
        inscricao_suframa=nfe_cliente.get(mapCliente("inscricao_suframa"), ""),
        razao_social=nfe_cliente.get(mapCliente("razao_social"), ""),
    )
    if nfe_cliente.get("CPF") and not nfe_cliente.get("CNPJ"):
        _cliente["tipo_documento"] = "CPF"
        _cliente["numero_documento"] = nfe_cliente.get("CPF")
    else:
        _cliente["tipo_documento"] = "CNPJ"
        _cliente["numero_documento"] = nfe_cliente.get("CNPJ")

    # .get('prod')
    produtos = mapProduto(nfe_dict)

    nfe_resp_tec = nfe_dict["infRespTec"]

    responsavel_tecnico = dict(
        cnpj=nfe_resp_tec["CNPJ"],
        contato=nfe_resp_tec["xContato"],
        email=nfe_resp_tec["email"],
        fone=nfe_resp_tec["fone"],
    )

    nfe_ref = nfe_dict["ide"]["NFref"]
    nfe_referenciada = dict(chave_acesso=nfe_ref["refNFe"])
    nota = nfe_dict["ide"]

    nfe_total = nfe_dict["total"]["ICMSTot"]
    total = dict(
        totais_icms_base_calculo=Decimal(nfe_total["vBC"]),
        totais_icms_total=Decimal(nfe_total["vICMS"]),
        totais_icms_desonerado=Decimal(nfe_total["vICMSDeson"]),
        totais_fcp_destino=Decimal(nfe_total["vFCPUFDest"]),
        totais_icms_inter_destino=Decimal(nfe_total["vICMSUFDest"]),
        totais_icms_inter_remetente=Decimal(nfe_total["vICMSUFRemet"]),
        totais_fcp=Decimal(nfe_total["vFCP"]),
        totais_icms_st_base_calculo=Decimal(nfe_total["vBCST"]),
        totais_icms_st_total=Decimal(nfe_total["vST"]),
        totais_fcp_st=Decimal(nfe_total["vFCPST"]),
        totais_fcp_st_ret=Decimal(nfe_total["vFCPSTRet"]),
        totais_icms_total_produtos_e_servicos=Decimal(nfe_total["vProd"]),
        totais_icms_total_frete=Decimal(nfe_total["vFrete"]),
        totais_icms_total_seguro=Decimal(nfe_total["vSeg"]),
        totais_icms_total_desconto=Decimal(nfe_total["vDesc"]),
        totais_icms_total_ii=Decimal(nfe_total["vII"]),
        totais_icms_total_ipi=Decimal(nfe_total["vIPI"]),
        totais_icms_total_ipi_dev=Decimal(nfe_total["vIPIDevol"]),
        totais_icms_pis=Decimal(nfe_total["vPIS"]),
        totais_icms_cofins=Decimal(nfe_total["vCOFINS"]),
        totais_icms_outras_despesas_acessorias=Decimal(nfe_total["vOutro"]),
        totais_icms_total_nota=Decimal(nfe_total["vNF"]),
    )

    _nota_fiscal = dict(
        uf=CODIGOS_ESTADOS_T[nota["cUF"]],
        codigo_numerico_aleatorio=nota["cNF"],
        natureza_operacao=nota["natOp"],
        modelo=int(nota["mod"]),
        serie=nota["serie"],
        numero_nf=nota["nNF"],
        data_emissao=datetime.now(),
        data_saida_entrada=datetime.now(),
        tipo_documento=nota["tpNF"],
        indicador_destino=nota["idDest"],
        municipio=nota["cMunFG"],
        tipo_impressao_danfe=nota["tpImp"],
        forma_emissao=nota["tpEmis"],
        ambiente=nota["tpAmb"],
        finalidade_emissao=nota["finNFe"],
        cliente_final=nota["indFinal"],
        indicador_presencial=nota["indPres"],
        processo_emissao=nota["procEmi"],
        transporte_modalidade_frete=nfe_dict["transp"]["modFrete"],
        tipo_pagamento=nfe_dict["pag"]["detPag"]["tPag"],
        informacoes_complementares_interesse_contribuinte=nfe_dict["infAdic"]["infCpl"],
        **total,
    )
    nota_fiscal_Pynfe = NotaFiscal(
        **_nota_fiscal,
        emitente=Emitente(**_emitente),
        cliente=Cliente(**_cliente),
    )
    nota_fiscal_Pynfe.adicionar_nota_fiscal_referenciada(**nfe_referenciada)
    for produto in produtos:
        nota_fiscal_Pynfe.adicionar_produto_servico(
            **produto,
        )

    # nota_fiscal_Pynfe.adicionar_transporte_volume(
    #     quantidade = Decimal(1),
    #     peso_liquido=nfe_dict["transp"]["vol"]["pesoL"],
    #     peso_bruto=nfe_dict["transp"]["vol"]["pesoB"],
    # )
    # vizualiza nota attrs:
    # pp({
    #     atr: getattr(nota_fiscal_Pynfe, atr)
    #     for atr in dir(nota_fiscal_Pynfe)
    #     if not atr.startswith("_")
    # })
    # ENVIA
    serializador = SerializacaoXML(_fonte_dados, homologacao=HOMOLOGACAO)
    nfe = serializador.exportar()

    # assinatura
    a1 = AssinaturaA1(CERTIFICADO, SENHA_CERTIFICADO)
    xml = a1.assinar(nfe)

    return xml


def autorização(xml_assinado: str):
    """recebe a xml assinada em formato string e a comunicação sefaz e retorna o "envio" result do pynfe"""
    _teste_configurado()

    xml_assinado = etree.fromstring(xml_assinado) # type: ignore
    xml_str = etree.tostring(xml_assinado, encoding="unicode") # type: ignore
    index_id = xml_str.find("Id=") + 7

    chave_de_acesso = xml_str[index_id : index_id + 44]
    _salva_log(
        chave_de_acesso + "notagerada", etree.tostring(xml_assinado, encoding="unicode") # type: ignore
    )  # type: ignore

    # envio
    if not IGNORA_PRODUCAO_WARNING and not HOMOLOGACAO:
        input("ENVIO DE NOTA FISCAL EM PRODUÇÃO, CONTINUAR? (SIM)")

    try:
        envio = con.autorizacao(modelo="nfe", nota_fiscal=xml_assinado)
    except Exception as e:
        _salva_log("erro_autorizacao" + chave_de_acesso, str(e))
        raise

    _salva_log(chave_de_acesso + "envio[1]", envio[1].text)
    _salva_log(
        chave_de_acesso + "envio[2]",
        etree.tostring(envio[2], encoding="unicode"),  # type: ignore
    )
    # pega
    recibo = envio[1].text
    pos_chave_recibo = recibo.find("<nRec>") + 6
    chave_recibo = recibo[pos_chave_recibo : pos_chave_recibo + 15]

    start_tMed = recibo.find("<tMed")
    final_tMed = recibo.find("</tMed")
    tMed = recibo[start_tMed + 6 : final_tMed]

    return chave_recibo, int(tMed), chave_de_acesso


def evento_cancelamento(
    cnpj, chave_acesso_nota_a_cancelar, uf, protocolo, justificativa
):
    """calelamento de nfe

    Args:
        cnpj (str): cnpj
        chave_acesso_nota_a_cancelar (str): chave de acesso da nota
        uf (str): estado SP
        protocolo (str): Informar o número do Protocolo de Autorização da NF-e a ser Cancelada. (vide item 5.8).
        justificativa (str): Informar a justificativa do cancelamento (min 15 max 255 caracteres)
    """

    cancelar = EventoCancelarNota(
        cnpj=cnpj,
        chave=chave_acesso_nota_a_cancelar,
        uf=uf,
        protocolo=protocolo,
        justificativa=justificativa,
        data_emissao=datetime.now(),
    )

    _salva_log(
        "cancelamento",
        "Cancelando nota "
        + chave_acesso_nota_a_cancelar
        + "justificativa: "
        + justificativa,
    )
    # serialização
    serializador = SerializacaoXML(_fonte_dados, homologacao=HOMOLOGACAO)
    nfe_cancel = serializador.serializar_evento(cancelar)
    # assinatura
    a1 = AssinaturaA1(CERTIFICADO, senha=SENHA_CERTIFICADO)
    xml = a1.assinar(nfe_cancel)
    _salva_log(
        f"cancelamento_{chave_acesso_nota_a_cancelar}",
        f"{etree.tostring(nfe_cancel,encoding='unicode' )}\n", # type: ignore
        eh_xml=True,
    )

    envio = con.evento(modelo="nfe", evento=xml)  # modelo='nfce' ou 'nfe'
    _salva_log("cancelamento", f"\n\n<!--resultado cancelamento no arquivo: cancelamento -->\n{chave_acesso_nota_a_cancelar}.xml\n")
    _salva_log(
        f"cancelamento_{chave_acesso_nota_a_cancelar}",
        f"{envio.text}",
        eh_xml=True,
    )

    return envio


def inutilizacao(modelo, cnpj, numero_inicial, numero_final, justificativa, serie):
    raise NotImplemented("inutilizacao não implementada corretamente, favor conferir")
    _salva_log(
        "inutilizacao_log",
        f"Inutilizando notas de {numero_inicial} a {numero_final}...\n",
    )
    response = con.inutilizacao(
        modelo=modelo,
        cnpj=cnpj,
        numero_inicial=numero_inicial,
        numero_final=numero_final,
        justificativa=justificativa,
        serie=serie,
    )
    __import__("ipdb").set_trace()
    _salva_log("inutilizacao_log", f"...notas inutilizadas\n{response.text}\n")
    return response


def consulta(chave):
    _teste_configurado()
    r = con.consulta_nota("nfe", chave)
    _salva_log(chave + "consulta_nota_result_", r.text)


def consulta_recibo(chave, chave_acesso, tMed):
    _teste_configurado()

    try:
        r = con.consulta_recibo("nfe", chave)
    except Exception as e:
        _salva_log("erro_consulta" + chave_acesso + chave, str(e))
        raise

    _salva_log(
        chave_acesso + "_" + chave + "consulta_recibo_result_",
        r.text,
        pasta="consultas",
    )
    return chave_acesso,r.text


def _salva_log(nome_arq: str, conteudo: str, pasta="log/pynfe_driver", eh_xml=False):
    now = datetime.now()
    os.makedirs(pasta, exist_ok=True)
    if GERA_LOG:
        with open(
            f"{pasta}/{nome_arq}_{DATETIME}.{'log' if not eh_xml else 'xml'}", "a"
        ) as f:
            f.write(
                f'{now.isoformat() if not eh_xml else "<!--"+now.isoformat()+"-->" } + {conteudo}'
                )


