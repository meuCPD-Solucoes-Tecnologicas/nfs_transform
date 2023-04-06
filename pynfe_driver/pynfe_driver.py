import datetime
from map4 import mapCliente, mapEmitente, mapProduto, mapaT
from nfe_as_dict import nfe_xml
from pynfe.entidades.notafiscal import NotaFiscal

HOMOLOGACAO = True
CERTIFICADO = "CERTIFICADO LUZ LED COMERCIO ONLINE_VENCE 13.05.2023(1).p12"
UF = "SP"


nfe_emit: dict = nfe_xml.get("emit")
emitente = dict(
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
cliente = dict(
    email=nfe_cliente.get(mapCliente("email")),
    endereco_bairro=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_bairro")),
    endereco_cep=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_cep")),
    endereco_cod_municipio=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_cod_municipio")
    ),
    endereco_complemento=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_complemento")
    ),
    endereco_logradouro=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_logradouro")
    ),
    endereco_municipio=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_municipio")
    ),
    endereco_numero=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_numero")),
    endereco_pais=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_pais")),
    endereco_telefone=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_telefone")
    ),
    endereco_uf=nfe_cliente.get("enderDest", {}).get(
        mapCliente("endereco_uf")),
    indicador_ie=nfe_cliente.get(mapCliente("indicador_ie")),
    inscricao_estadual=nfe_cliente.get(mapCliente("inscricao_estadual")),
    inscricao_municipal=nfe_cliente.get(mapCliente("inscricao_municipal")),
    inscricao_suframa=nfe_cliente.get(mapCliente("inscricao_suframa")),
    #  isento_icms=nfe_cliente.get(mapCliente('isento_icms'),''),
    razao_social=nfe_cliente.get(mapCliente("razao_social")),
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
    valor_unitario_comercial=nfe_produto.get("vUnCom"),
    valor_total_bruto=nfe_produto.get("vProd"),
    ean_tributavel=nfe_produto.get("cEANTrib"),
    unidade_tributavel=nfe_produto.get("uTrib"),
    quantidade_tributavel=nfe_produto.get("qTrib"),
    valor_unitario_tributavel=nfe_produto.get("vUnTrib"),
    ind_total=nfe_produto.get("indTot"),
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

# dessseriealize pra esse dict  segundo as atribuições abaixo
#total": {
        # "ICMSTot": {
        #     "vBC": "159.90",
        #     "vICMS": "6.40",
        #     "vICMSDeson": "0.00",
        #     "vFCPUFDest": "0.00",
        #     "vICMSUFDest": "0.00",
        #     "vICMSUFRemet": "0.00",
        #     "vFCP": "0.00",
        #     "vBCST": "0.00",
        #     "vST": "0.00",
        #     "vFCPST": "0.00",
        #     "vFCPSTRet": "0.00",
        #     "vProd": "0.00",
        #     "vFrete": "0.00",
        #     "vSeg": "0.00",
        #     "vDesc": "0.00",
        #     "vII": "0.00",
        #     "vIPI": "0.00",
        #     "vIPIDevol": "0.00",
        #     "vPIS": "0.00",
        #     "vCOFINS": "0.00",
        #     "vOutro": "0.00",
        #     "vNF": "0.00",
        # }
        
# atribuições:
# total = etree.SubElement(raiz, 'total')
#         icms_total = etree.SubElement(total, 'ICMSTot')
#         etree.SubElement(icms_total, 'vBC').text = '{:.2f}'.format(nota_fiscal.totais_icms_base_calculo)
#         etree.SubElement(icms_total, 'vICMS').text = '{:.2f}'.format(nota_fiscal.totais_icms_total)
#         etree.SubElement(icms_total, 'vICMSDeson').text = '{:.2f}'.format(nota_fiscal.totais_icms_desonerado)  # Valor Total do ICMS desonerado
#         if nota_fiscal.totais_fcp_destino:
#             etree.SubElement(icms_total, 'vFCPUFDest').text = '{:.2f}'.format(nota_fiscal.totais_fcp_destino)
#         if nota_fiscal.totais_icms_inter_destino:
#             etree.SubElement(icms_total, 'vICMSUFDest').text = '{:.2f}'.format(nota_fiscal.totais_icms_inter_destino)
#         if nota_fiscal.totais_icms_inter_remetente:
#             etree.SubElement(icms_total, 'vICMSUFRemet').text = '{:.2f}'.format(nota_fiscal.totais_icms_remetente)
#         etree.SubElement(icms_total, 'vFCP').text = '{:.2f}'.format(nota_fiscal.totais_fcp)
#         etree.SubElement(icms_total, 'vBCST').text = '{:.2f}'.format(nota_fiscal.totais_icms_st_base_calculo)
#         etree.SubElement(icms_total, 'vST').text = '{:.2f}'.format(nota_fiscal.totais_icms_st_total)
#         etree.SubElement(icms_total, 'vFCPST').text = '{:.2f}'.format(nota_fiscal.totais_fcp_st)
#         etree.SubElement(icms_total, 'vFCPSTRet').text = '{:.2f}'.format(nota_fiscal.totais_fcp_st_ret)
#         etree.SubElement(icms_total, 'vProd').text = str(nota_fiscal.totais_icms_total_produtos_e_servicos)
#         etree.SubElement(icms_total, 'vFrete').text = '{:.2f}'.format(nota_fiscal.totais_icms_total_frete)
#         etree.SubElement(icms_total, 'vSeg').text = '{:.2f}'.format(nota_fiscal.totais_icms_total_seguro)
#         etree.SubElement(icms_total, 'vDesc').text = '{:.2f}'.format(nota_fiscal.totais_icms_total_desconto)

#         # Tributos
#         etree.SubElement(icms_total, 'vII').text = '{:.2f}'.format(nota_fiscal.totais_icms_total_ii)
#         etree.SubElement(icms_total, 'vIPI').text = '{:.2f}'.format(nota_fiscal.totais_icms_total_ipi)
#         etree.SubElement(icms_total, 'vIPIDevol').text = '{:.2f}'.format(nota_fiscal.totais_icms_total_ipi_dev)
#         etree.SubElement(icms_total, 'vPIS').text = '{:.2f}'.format(nota_fiscal.totais_icms_pis)
#         etree.SubElement(icms_total, 'vCOFINS').text = '{:.2f}'.format(nota_fiscal.totais_icms_cofins)

#         etree.SubElement(icms_total, 'vOutro').text = '{:.2f}'.format(nota_fiscal.totais_icms_outras_despesas_acessorias)
#         etree.SubElement(icms_total, 'vNF').text = str(nota_fiscal.totais_icms_total_nota)
#         if nota_fiscal.totais_tributos_aproximado:
#             etree.SubElement(icms_total, 'vTotTrib').text = '{:.2f}'.format(nota_fiscal.totais_tributos_aproximado)


nfe_total = nfe_xml['total']["ICMSTot"]
total = dict(
    
    totais_icms_base_calculo=nfe_total["vBC"], #etree.SubElement(icms_total, 'vBC').text (linha 185)
    totais_icms_total=nfe_total["vICMS"], #etree.SubElement(icms_total, 'vICMS').text (linha 186)
    totais_icms_desonerado=nfe_total["vICMSDeson"], #etree.SubElement(icms_total, 'vICMSDeson').text (linha 187)
    totais_fcp_destino=nfe_total["vFCPUFDest"], #etree.SubElement(icms_total, 'vFCPUFDest').text (linha 188)
    totais_icms_inter_destino=nfe_total["vICMSUFDest"], #etree.SubElement(icms_total, 'vICMSUFDest').text (linha 189)
    totais_icms_inter_remetente=nfe_total["vICMSUFRemet"], #etree.SubElement(icms_total, 'vICMSUFRemet').text (linha 190)
    totais_fcp=nfe_total["vFCP"], #etree.SubElement(icms_total, 'vFCP').text (linha 191)
    totais_icms_st_base_calculo=nfe_total["vBCST"], #etree.SubElement(icms_total, 'vBCST').text (linha 192)
    totais_icms_st_total=nfe_total["vST"], #etree.SubElement(icms_total, 'vST').text (linha 193)
    totais_fcp_st=nfe_total["vFCPST"], #etree.SubElement(icms_total, 'vFCPST').text (linha 194)
    totais_fcp_st_ret=nfe_total["vFCPSTRet"], #etree.SubElement(icms_total, 'vFCPSTRet').text (linha 195)
    totais_icms_total_produtos_e_servicos=nfe_total["vProd"], #etree.SubElement(icms_total, 'vProd').text (linha 196)
    totais_icms_total_frete=nfe_total["vFrete"], #etree.SubElement(icms_total, 'vFrete').text (linha 197)
    totais_icms_total_seguro=nfe_total["vSeg"], #etree.SubElement(icms_total, 'vSeg').text (linha 198)
    totais_icms_total_desconto=nfe_total["vDesc"], #etree.SubElement(icms_total, 'vDesc').text (linha 199)
    totais_icms_total_ii=nfe_total["vII"], #etree.SubElement(icms_total, 'vII').text (linha 200)
    totais_icms_total_ipi=nfe_total["vIPI"], #etree.SubElement(icms_total, 'vIPI').text (linha 201)
    totais_icms_total_ipi_dev=nfe_total["vIPIDevol"], #etree.SubElement(icms_total, 'vIPIDevol').text (linha 202)
    totais_icms_pis=nfe_total["vPIS"], #etree.SubElement(icms_total, 'vPIS').text (linha 203)
    totais_icms_cofins=nfe_total["vCOFINS"], #etree.SubElement(icms_total, 'vCOFINS').text (linha 204)
    totais_icms_outras_despesas_acessorias=nfe_total["vOutro"], #etree.SubElement(icms_total, 'vOutro').text (linha 205)
    totais_icms_total_nota=nfe_total["vNF"], #etree.SubElement(icms_total, 'vNF').text (linha 206)
    #totais_tributos_aproximado=nfe_total["vTotTrib"], #etree.SubElement(icms_total, 'vTotTrib').text (linha 207)



)

#     "transp": {"modFrete": "9", "vol": {"pesoL": "0.000", "pesoB": "0.000"}},

nfe_transporte = nfe_xml['transp']
transporte = dict(

    transportadora_modalidade_frete=nfe_transporte["modFrete"],
    transportadora_volume_peso_liquido=nfe_transporte["vol"]["pesoL"], 
    transportadora_volume_peso_bruto=nfe_transporte["vol"]["pesoB"], 

)

#"pag": {"detPag": {"tPag": "90", "vPag": "0"}}
nfe_pagamento = nfe_xml['pag']

pagamento = dict(

    pagamento_tipo=nfe_pagamento["detPag"]["tPag"], 
    pagamento_valor=nfe_pagamento["detPag"]["vPag"], 

)

# #"infRespTec": {
#         "CNPJ": "15088992000128",
#         "xContato": "Fernando",
#         "email": "integracao@tiny.com.br",
#         "fone": "05430558200",
#     }

nfe_resp_tec = nfe_xml['infRespTec']

responsavel_tecnico = dict(

    cnpj=nfe_resp_tec["CNPJ"],
    contato=nfe_resp_tec["xContato"],
    email=nfe_resp_tec["email"],
    fone=nfe_resp_tec["fone"],
    
    
)

# #"infAdic": {
#         "infCpl": 'Conforme artigo 182 IV do RICMS, Nota fiscal complementar de ICMS referente a NF "*116*" da serie "*01*" de "*31/08/2022*".'
#     }

nota_referenciada = dict(
    tipo = str() ,# - Tipo (seleciona de lista) - NF_REFERENCIADA_TIPOS
    chave_acesso = str(),#  - Nota Fiscal eletronica - Chave de Acesso
    uf = str(),# - Nota Fiscal - UF
    mes_ano_emissao = str(),#   - Mes e ano de emissao
    cnpj = str(),#   - CNPJ
    serie = str(),#   - Serie (XXX)
    numero = str(),#   - Numero
    modelo = str(),#   - Modelo
)
# class NotaFiscalReferenciada(Entidade):
# desserialize os campos asseguir  a apartir do serializador abaixo
# cUF
# cNF
# natOp
# mod
# serie
# nNF
# dhEmi
# tpNF
# idDest
# cMunFG
# tpImp
# tpEmis
# cDV
# tpAmb
# finNFe
# indFinal
# indPres
# procEmi
# verProc
# NFref

# serializador
#  # Dados da Nota Fiscal
#         ide = etree.SubElement(raiz, 'ide')
#         etree.SubElement(ide, 'cUF').text = CODIGOS_ESTADOS[nota_fiscal.uf]
#         etree.SubElement(ide, 'cNF').text = nota_fiscal.codigo_numerico_aleatorio
#         etree.SubElement(ide, 'natOp').text = nota_fiscal.natureza_operacao
#         etree.SubElement(ide, 'mod').text = str(nota_fiscal.modelo)
#         etree.SubElement(ide, 'serie').text = nota_fiscal.serie
#         etree.SubElement(ide, 'nNF').text = str(nota_fiscal.numero_nf)
#         etree.SubElement(ide, 'dhEmi').text = nota_fiscal.data_emissao.strftime('%Y-%m-%dT%H:%M:%S') + tz
#         # Apenas NF-e
#         if nota_fiscal.modelo == 55:
#             if nota_fiscal.data_saida_entrada:
#                 etree.SubElement(ide, 'dhSaiEnt').text = nota_fiscal.data_saida_entrada.strftime('%Y-%m-%dT%H:%M:%S') + tz
#             """dhCont Data e Hora da entrada em contingência E B01 D 0-1 Formato AAAA-MM-DDThh:mm:ssTZD (UTC - Universal
#                 Coordinated Time)
#                 Exemplo: no formato UTC para os campos de Data-Hora, "TZD" pode ser -02:00 (Fernando de Noronha), -03:00 (Brasília) ou -04:00 (Manaus), no
#                 horário de verão serão -01:00, -02:00 e -03:00. Exemplo: "2010-08-19T13:00:15-03:00".
#             """
#         etree.SubElement(ide, 'tpNF').text = str(nota_fiscal.tipo_documento)  # 0=entrada 1=saida
#         """ nfce suporta apenas operação interna
#             Identificador de local de destino da operação 1=Operação interna;2=Operação interestadual;3=Operação com exterior.
#         """
#         if nota_fiscal.modelo == 65:
#             etree.SubElement(ide, 'idDest').text = str(1)
#         else:
#             etree.SubElement(ide, 'idDest').text = str(nota_fiscal.indicador_destino)
#         etree.SubElement(ide, 'cMunFG').text = nota_fiscal.municipio
#         etree.SubElement(ide, 'tpImp').text = str(nota_fiscal.tipo_impressao_danfe)
#         """ ### CONTINGENCIA ###
#             1=Emissão normal (não em contingência);
#             2=Contingência FS-IA, com impressão do DANFE em formulário de segurança;
#             3=Contingência SCAN (Sistema de Contingência do Ambiente Nacional);
#             4=Contingência DPEC (Declaração Prévia da Emissão em Contingência);
#             5=Contingência FS-DA, com impressão do DANFE em formulário de segurança;
#             6=Contingência SVC-AN (SEFAZ Virtual de Contingência do AN);
#             7=Contingência SVC-RS (SEFAZ Virtual de Contingência do RS);
#             9=Contingência off-line da NFC-e (as demais opções de contingência são válidas também para a NFC-e).
#             Para a NFC-e somente estão disponíveis e são válidas as opções de contingência 5 e 9.
#         """
#         if self._contingencia != None:
#             if nota_fiscal.forma_emissao == '1':
#                 nota_fiscal.forma_emissao = '9'
#         etree.SubElement(ide, 'tpEmis').text = str(nota_fiscal.forma_emissao)
#         etree.SubElement(ide, 'cDV').text = nota_fiscal.dv_codigo_numerico_aleatorio
#         etree.SubElement(ide, 'tpAmb').text = str(self._ambiente)
#         etree.SubElement(ide, 'finNFe').text = str(nota_fiscal.finalidade_emissao)
nota = nfe_xml['ide']
nota_fiscal = dict(
    uf = nota['cUF'] # (linha 321) etree.SubElement(ide, 'cUF').text = CODIGOS_ESTADOS[nota_fiscal.uf]
    codigo_numerico_aleatorio = nota['cNF'] # (linha 322)  etree.SubElement(ide, 'cNF').text = nota_fiscal.codigo_numerico_aleatorio
    natureza_operacao = nota['natOp'] # (linha 323) etree.SubElement(ide, 'natOp').text = nota_fiscal.natureza_operacao
    modelo = nota['mod'] # (linha 324) etree.SubElement(ide, 'mod').text = str(nota_fiscal.modelo)
    serie = nota['serie'] # (linha 325) etree.SubElement(ide, 'serie').text = nota_fiscal.serie
    numero_nf = nota['nNF'] # (linha 326) etree.SubElement(ide, 'nNF').text = str(nota_fiscal.numero_nf)
    data_emissao=datetime.datetime.now(),
    data_saida_entrada=datetime.datetime.now(),
    tipo_documento = nota['tpNF'] # (linha 337)
    indicador_destino = nota['idDest'] # (linha 329)
    municipio = nota['cMunFG'] # (linha 330)
    tipo_impressao_danfe = nota['tpImp'] # (linha 331)
    forma_emissao = nota['tpEmis'] # (linha 332)
    dv_codigo_numerico_aleatorio = nota['cDV'] # (linha 333)
    ambiente = nota['tpAmb'] # (linha 334)
    finalidade_emissao = nota['finNFe'] # (linha 335)
    indFinal = nota['indFinal'] # (linha 336)
    indPres = nota['indPres'] # (linha 337)
    procEmi = nota['procEmi'] # (linha 338)
    verProc = nota['verProc'] # (linha 339)
    NFref = nota['NFref'] # (linha 340
)


nfe_referenciada


