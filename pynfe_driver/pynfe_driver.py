from datetime import datetime
from decimal import Decimal
from pprint import pp
try:
    from .map4 import mapCliente, mapEmitente, mapProduto, mapaT
except ImportError:
    from map4 import mapCliente, mapEmitente, mapProduto, mapaT

from pynfe.entidades.fonte_dados import _fonte_dados
from pynfe.entidades.notafiscal import NotaFiscal
from pynfe.entidades import *
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.utils.flags import CODIGOS_ESTADOS
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoSefaz
import os
import re


from lxml import etree

HOMOLOGACAO: bool
CERTIFICADO: str
UF = "SP"
CODIGOS_ESTADOS_T = {v: k for k, v in CODIGOS_ESTADOS.items()}
PASTA_LOG = 'log'
IGNORA_HOMOLOGACAO_WARNING: bool

con: ComunicacaoSefaz
log: bool

def log_Seerro(msg,xml):
    """Salva XML que deu erro de acordo com uma mensagem de erro.
    template xml:
    

    Args:
        msg (str): Mensagem de erro.
        xml (str): XML que deu erro.
    """
    xml_proc = xml[str(xml).find('<protNFe '):str(xml).find('</protNFe>')+10]
    
    motivo = xml_proc[str(xml_proc).find('<xMotivo>')+9:str(xml_proc).find('</xMotivo>')]
    chNfe = xml_proc[str(xml_proc).find('<chNFe>')+7:str(xml_proc).find('</chNFe>')]
    

    if motivo and msg!=motivo:
        #verifica se existe o arquivo errors.log
        if not os.path.exists('errors.log'):
            with open('errors.log','w') as f:
                f.write('')
        
        with open(os.path.join(PASTA_LOG,"errors.log"),'a') as f:
            f.write(datetime.now().isoformat()+":"+chNfe+" "+motivo+"\n")
            


def configura(
        caminho_certificado: str,
        senha_certificado: str,
        ambiente_homologacao=True,
        uf='SP',
        gera_log=True,
        ignora_homologacao_warning=False
):
    global HOMOLOGACAO
    global con
    global log
    global IGNORA_HOMOLOGACAO_WARNING
    global CERTIFICADO

    # os file exists
    if not os.path.exists(caminho_certificado):
        raise Exception('Certificado não encontrado\n'+caminho_certificado)

    CERTIFICADO = caminho_certificado

    IGNORA_HOMOLOGACAO_WARNING = ignora_homologacao_warning
    log = gera_log
    con = ComunicacaoSefaz(
        uf,
        caminho_certificado,
        senha_certificado,
        ambiente_homologacao
    )
    HOMOLOGACAO = ambiente_homologacao
    # return


def _teste_configurado():
    if (HOMOLOGACAO is None):
        raise Exception('HOMOLOGACAO não configurados')
    if (con is None):
        raise Exception('con não configurados')
    if (log is None):
        raise Exception('log não configurados')
    if (IGNORA_HOMOLOGACAO_WARNING is None):
        raise Exception('IGNORA_HOMOLOGACAO_WARNING não configurados')


def converte_para_pynfe_XML_assinado(nfe_dict: dict) -> etree.Element:
    _teste_configurado()

    try:
        nfe_dict = nfe_dict['nfeProc']['NFe']['infNFe']
    except:
        nfe_dict = nfe_dict['NFe']['infNFe']

    nfe_emit: dict = nfe_dict["emit"]

    _emitente = dict(
        cnae_fiscal=nfe_emit.get(mapEmitente("cnae_fiscal")),
        cnpj=nfe_emit.get(mapEmitente("cnpj")),
        codigo_de_regime_tributario=nfe_emit.get(
            mapEmitente("codigo_de_regime_tributario")
        ),
        endereco_bairro=nfe_emit.get("enderEmit", {}).get(
            mapEmitente("endereco_bairro")),
        endereco_cep=nfe_emit.get("enderEmit", {}).get(
            mapEmitente("endereco_cep")),
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
            mapEmitente("endereco_numero")),
        endereco_pais=nfe_emit.get("enderEmit", {}).get(
            mapEmitente("endereco_pais")),
        endereco_telefone=nfe_emit.get("enderEmit", {}).get(
            mapEmitente("endereco_telefone")
        ),
        endereco_uf=nfe_emit.get("enderEmit", {}).get(
            mapEmitente("endereco_uf")),
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
            mapCliente("endereco_bairro"), ""),
        endereco_cep=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_cep"), ""),
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
            mapCliente("endereco_numero"), ""),
        endereco_pais=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_pais"), ""),
        endereco_telefone=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_telefone"), ""
        ),
        endereco_uf=nfe_cliente.get("enderDest", {}).get(
            mapCliente("endereco_uf"), ""),
        indicador_ie=int(nfe_cliente.get(mapCliente("indicador_ie"), "")),
        inscricao_estadual=nfe_cliente.get(mapCliente("inscricao_estadual")),
        inscricao_municipal=nfe_cliente.get(
            mapCliente("inscricao_municipal"), ""),
        inscricao_suframa=nfe_cliente.get(mapCliente("inscricao_suframa"), ""),

        razao_social=nfe_cliente.get(mapCliente("razao_social"), ""),
    )
    if nfe_cliente.get("CPF") and not nfe_cliente.get("CNPJ"):
        _cliente['tipo_documento'] = "CPF"
        _cliente['numero_documento'] = nfe_cliente.get("CPF")
    else:
        _cliente['tipo_documento'] = "CNPJ"
        _cliente['numero_documento'] = nfe_cliente.get("CNPJ")

    # .get('prod')
    produtos = mapProduto(nfe_dict)

    nfe_resp_tec = nfe_dict['infRespTec']

    responsavel_tecnico = dict(

        cnpj=nfe_resp_tec["CNPJ"],
        contato=nfe_resp_tec["xContato"],
        email=nfe_resp_tec["email"],
        fone=nfe_resp_tec["fone"],


    )

    nfe_ref = nfe_dict['ide']['NFref']
    nfe_referenciada = dict(
        chave_acesso=nfe_ref['refNFe']
    )
    nota = nfe_dict['ide']

    nfe_total = nfe_dict['total']["ICMSTot"]
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
        totais_icms_total_nota=Decimal(nfe_total["vNF"])


    )

    _nota_fiscal = dict(
        uf=CODIGOS_ESTADOS_T[nota['cUF']],
        codigo_numerico_aleatorio=nota['cNF'],
        natureza_operacao=nota['natOp'],
        modelo=int(nota['mod']),
        serie=nota['serie'],
        numero_nf=nota['nNF'],
        data_emissao=datetime.now(),
        data_saida_entrada=datetime.now(),
        tipo_documento=nota['tpNF'],
        indicador_destino=nota['idDest'],
        municipio=nota['cMunFG'],
        tipo_impressao_danfe=nota['tpImp'],
        forma_emissao=nota['tpEmis'],
        ambiente=nota['tpAmb'],
        finalidade_emissao=nota['finNFe'],
        cliente_final=nota['indFinal'],
        indicador_presencial=nota['indPres'],
        processo_emissao=nota['procEmi'],
        transporte_modalidade_frete=nfe_dict['transp']["modFrete"],
        tipo_pagamento=nfe_dict['pag']["detPag"]["tPag"],
        informacoes_complementares_interesse_contribuinte=nfe_dict['infAdic']['infCpl'],
        **total
    )
    nota_fiscal_Pynfe = NotaFiscal(
        **_nota_fiscal,
        emitente=Emitente(**_emitente),
        cliente=Cliente(**_cliente),

    )
    nota_fiscal_Pynfe.adicionar_nota_fiscal_referenciada(
        **nfe_referenciada
    )
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
    a1 = AssinaturaA1(CERTIFICADO, '123456')
    xml = a1.assinar(nfe)

    return xml


def autorização(xml_assinado):
    """recebe a xml assinada e a comunicação sefaz e retorna o "envio" result do pynfe"""
    _teste_configurado()


    xml_str = etree.tostring(xml_assinado,encoding='unicode')
    index_id = xml_str.find("Id=")+7

    chave = xml_str[index_id:index_id+44]
    # _salva_log(chave+'notagerada',
    #            etree.tostring(xml_assinado, encoding='unicode'))  # type: ignore

    # envio
    if not IGNORA_HOMOLOGACAO_WARNING and not HOMOLOGACAO:
        input('ENVIO DE NOTA FISCAL EM PRODUÇÃO, CONTINUAR? (SIM)')

    try:
        envio = con.autorizacao(modelo='nfe', nota_fiscal=xml_assinado)
    except Exception as e:
        _salva_log('erro_autorizacao'+chave,str(e))
        raise
    
    _salva_log(chave+'envio[1]', envio[1].text)
    _salva_log(chave+'envio[2]', etree.tostring(
        envio[2],
        encoding='unicode')  # type: ignore
    )
    # pega
    recibo = envio[1].text
    pos_chave_recibo = recibo.find('<nRec>')+6
    chave_recibo = recibo[pos_chave_recibo:pos_chave_recibo+15]
    
    start_tMed = recibo.find('<tMed')
    final_tMed = recibo.find('</tMed')
    tMed = recibo[start_tMed+6:final_tMed]

    return chave_recibo,int(tMed)


def consulta(chave):
    _teste_configurado()
    r = con.consulta_nota(
        'nfe',
        chave
    )
    _salva_log(chave+'consulta_nota_result_', r.text)


def consulta_recibo(chave):
    _teste_configurado()
    
    try:
        r = con.consulta_recibo(
            'nfe',
            chave
        )
    except Exception as e:
        _salva_log('erro_consulta'+chave,str(e))
        raise
    
    
    # log_Seerro("Rejeição: Chave de Acesso referenciada inexistente [nRef: 1]"
    #            , r.text)
    _salva_log(chave+'consulta_recibo_result_', r.text,pasta='consultas')


def _salva_log(nome_arq, conteudo: str,pasta='log'):
    formatted_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S:%f")
    if log:
        open(f'{pasta}/{nome_arq}_{formatted_date}.xml', 'w+').write(conteudo)
# main()
# última consulta de quinta
# consulta_recibo('351011076380621')


# prod
# consulta_recibo('351011075323498')
# consulta('35230446364058000115550010000027081819212617')
