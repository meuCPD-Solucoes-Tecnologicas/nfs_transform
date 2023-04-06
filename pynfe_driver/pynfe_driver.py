import datetime
from decimal import Decimal
from pprint import pp
from .map4 import mapCliente, mapEmitente, mapProduto, mapaT
from .nfe_as_dict import nfe_xml
from pynfe.entidades.fonte_dados import _fonte_dados
from pynfe.entidades.notafiscal import NotaFiscal
from pynfe.entidades import *
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.utils.flags import CODIGOS_ESTADOS
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoSefaz


HOMOLOGACAO = True
CERTIFICADO = "CERTIFICADO LUZ LED COMERCIO ONLINE_VENCE 13.05.2023(1).p12"
UF = "SP"
CODIGOS_ESTADOS_T = {v: k for k, v in CODIGOS_ESTADOS.items()}

nfe_emit: dict = nfe_xml.get("emit")
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
    endereco_uf=nfe_emit.get("enderEmit", {}).get(mapEmitente("endereco_uf")),
    inscricao_estadual=nfe_emit.get(mapEmitente("inscricao_estadual")),
    inscricao_estadual_subst_tributaria=nfe_emit.get(
        mapEmitente("inscricao_estadual_subst_tributaria")
    ),
    inscricao_municipal=nfe_emit.get(mapEmitente("inscricao_municipal")),
    nome_fantasia=nfe_emit.get(mapEmitente("nome_fantasia")),
    razao_social=nfe_emit.get(mapEmitente("razao_social")),
)


nfe_cliente: dict = nfe_xml.get("dest")
_cliente = dict(
    email=nfe_cliente.get(mapCliente("email"),""),
    endereco_bairro=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_bairro"),""),
    endereco_cep=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_cep"),""),
    endereco_cod_municipio=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_cod_municipio"),""
    ),
    endereco_complemento=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_complemento"),""
    ),
    endereco_logradouro=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_logradouro"),""
    ),
    endereco_municipio=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_municipio"),""
    ),
    endereco_numero=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_numero"),""),
    endereco_pais=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_pais"),""),
    endereco_telefone=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_telefone"),""
    ),
    endereco_uf=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_uf"),""),
    indicador_ie=nfe_cliente.get(mapCliente("indicador_ie"),""),
    inscricao_estadual=nfe_cliente.get(mapCliente("inscricao_estadual"),""),
    inscricao_municipal=nfe_cliente.get(mapCliente("inscricao_municipal"),""),
    inscricao_suframa=nfe_cliente.get(mapCliente("inscricao_suframa"),""),

    razao_social=nfe_cliente.get(mapCliente("razao_social"),""),
)
if nfe_cliente.get("CPF") and nfe_cliente.get("CNPJ"):
    tipo_documento = "CPF"
    numero_documento = nfe_cliente.get("CPF")
else:
    tipo_documento = "CNPJ"
    numero_documento = nfe_cliente.get("CNPJ")


nfe_produto = nfe_xml.get("det").get('prod')

produto = dict(
    codigo=nfe_produto.get("cProd"),
    ean=nfe_produto.get("cEAN"),
    descricao=nfe_produto.get("xProd"),
    ncm=nfe_produto.get("NCM"),
    cfop=nfe_produto.get("CFOP"),
    unidade_comercial=nfe_produto.get("uCom"),
    quantidade_comercialor=nfe_produto.get("qCom"),
    valor_unitario_comercial=Decimal(nfe_produto.get("vUnCom")),
    valor_total_bruto=Decimal(nfe_produto.get("vProd")),
    ean_tributavel=nfe_produto.get("cEANTrib"),
    unidade_tributavel=nfe_produto.get("uTrib"),
    quantidade_tributavel=nfe_produto.get("qTrib"),
    valor_unitario_tributavel=Decimal(nfe_produto.get("vUnTrib")),
    ind_total=nfe_produto.get("indTot"),
    valor_tributos_aprox=''
)


imposto = nfe_xml['det']["imposto"]["ICMS"]["ICMS00"]
icms = dict(
    icms_modalidade=imposto.get('CST'),
    icms_aliquota=imposto.get('pICMS'),
    icms_valor=imposto.get('vICMS'),
    fcp_base_calculo=imposto.get('vBCFCP'),
    icms_st_percentual_reducao_bc=imposto.get('pRedBCST'),
    icms_st_valor_base_calculo=imposto.get('vBCST'),
    icms_st_aliquota=imposto.get('pICMSST'),
    icms_st_valor=imposto.get('vICMSST'),
    fcp_st_base_calculo=imposto.get('vBCFCPST'),
    icms_valor_base_calculo=imposto.get('vBC'),
    icms_desonerado=imposto.get('vICMSDeson'),
    icms_origem=imposto.get('orig'),
    icms_modalidade_determinacao_bc=imposto.get('modBC'),
    icms_st_modalidade_determinacao_bc=imposto.get('modBCST')
)

nfe_ipi = nfe_xml['det']["imposto"]["IPI"]

ipi = dict(
    ipi_classe_enquadramento=nfe_ipi.get('cEnq'),
    ipi_codigo_enquadramento=nfe_ipi.get('CST')
)

nfe_confins = nfe_xml['det']["imposto"]['COFINS']["COFINSOutr"]
confins = dict(
    cofins_modalidade=nfe_confins.get('CST'),
    cofins_valor_base_calculo=nfe_confins.get('vBC'),
    cofins_aliquota_percentual=nfe_confins.get('pCOFINS'),
    cofins_valor=nfe_confins.get('vCOFINS'),
)

nfe_pis = nfe_xml['det']["imposto"]['PIS']["PISOutr"]
pis = dict(

    pis_modalidade=nfe_pis["CST"],
    pis_valor_base_calculo=nfe_pis["vBC"],
    pis_aliquota_percentual=nfe_pis["pPIS"],
    pis_valor=nfe_pis["vPIS"],
)

nfe_total = nfe_xml['total']["ICMSTot"]
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



nfe_pagamento = nfe_xml['pag']

pagamento = dict(

    pagamento_tipo=nfe_pagamento["detPag"]["tPag"],
    pagamento_valor=nfe_pagamento["detPag"]["vPag"],

)


nfe_resp_tec = nfe_xml['infRespTec']

responsavel_tecnico = dict(

    cnpj=nfe_resp_tec["CNPJ"],
    contato=nfe_resp_tec["xContato"],
    email=nfe_resp_tec["email"],
    fone=nfe_resp_tec["fone"],


)

nfe_ref = nfe_xml['ide']['NFref']
nfe_referenciada = dict(
    chave_acesso=nfe_ref['refNFe']
)
nota = nfe_xml['ide']

_nota_fiscal = dict(
    uf=CODIGOS_ESTADOS_T[nota['cUF']],
    codigo_numerico_aleatorio=nota['cNF'],
    natureza_operacao=nota['natOp'],
    modelo=nota['mod'],
    serie=nota['serie'],
    numero_nf=nota['nNF'],
    data_emissao=datetime.datetime.now(),
    data_saida_entrada=datetime.datetime.now(),
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
    transporte_modalidade_frete=nfe_xml['transp']["modFrete"],
)
nota_fiscal_Pynfe = NotaFiscal(
    **_nota_fiscal,
    emitente=Emitente(**_emitente),
    cliente=Cliente(**_cliente),
)
nota_fiscal_Pynfe.adicionar_nota_fiscal_referenciada(
    **nfe_referenciada
)
nota_fiscal_Pynfe.adicionar_produto_servico(
    **produto,
    **total
)
nota_fiscal_Pynfe.adicionar_transporte_volume(
    peso_liquido=nfe_xml["transp"]["vol"]["pesoL"],
    peso_bruto=nfe_xml["transp"]["vol"]["pesoB"],
)
# vizualiza nota attrs:
pp({
    atr:getattr(nota_fiscal_Pynfe,atr)
    for atr in dir(nota_fiscal_Pynfe)
    if not atr.startswith("_")
})
# ENVIA
serializador = SerializacaoXML(_fonte_dados, homologacao=HOMOLOGACAO)
nfe = serializador.exportar()

# assinatura
a1 = AssinaturaA1(CERTIFICADO, '123456')
xml = a1.assinar(nfe)

from lxml import etree
open('notagerada.xml','w').write(etree.tostring( xml,encoding='unicode'))

# envio
con = ComunicacaoSefaz('SP', CERTIFICADO, '123456', HOMOLOGACAO)
envio = con.autorizacao(modelo='nfe', nota_fiscal=xml)
open('result.xml','w').write(envio[1].text)

breakpoint()
