from decimal import Decimal


mapa = {
    "cUF": "uf",
    "cNF": "codigo_numerico_aleatorio",
    "natOp": "natureza_operacao",
    "mod": "modelo",
    "serie": "serie",
    "nNF": "numero_nf",
    "dhEmi": "data_emissao",
    "dhSaiEnt": "data_saida_entrada",
    "tpNF": "tipo_documento",
    "idDest": "indicador_destino",
    "cMunFG": "municipio",
    "tpImp": "tipo_impressao_danfe",
    "tpEmis": "forma_emissao",
    "cDV": "dv_codigo_numerico_aleatorio",
    "finNFe": "finalidade_emissao",
    "indFinal": "cliente_final",
    "indPres": "indicador_presencial",
    "indIntermed": "indicador_intermediador",
    "procEmi": "processo_emissao",
    "verProc": "versao_processo_emissao",
    "dhCont": "data_emissao",
    "vBC": "totais_icms_base_calculo",
    "vICMS": "totais_icms_total",
    "vICMSDeson": "totais_icms_desonerado",
    "vFCPUFDest": "totais_fcp_destino",
    "vICMSUFDest": "totais_icms_inter_destino",
    "vICMSUFRemet": "totais_icms_remetente",
    "vFCP": "totais_fcp",
    "vBCST": "totais_icms_st_base_calculo",
    "vST": "totais_icms_st_total",
    "vFCPST": "totais_fcp_st",
    "vFCPSTRet": "totais_fcp_st_ret",
    "vProd": "totais_icms_total_produtos_e_servicos",
    "vFrete": "totais_icms_total_frete",
    "vSeg": "totais_icms_total_seguro",
    "vDesc": "totais_icms_total_desconto",
    "vII": "totais_icms_total_ii",
    "vIPI": "totais_icms_total_ipi",
    "vIPIDevol": "totais_icms_total_ipi_dev",
    "vPIS": "totais_icms_pis",
    "vCOFINS": "totais_icms_cofins",
    "vOutro": "totais_icms_outras_despesas_acessorias",
    "vNF": "totais_icms_total_nota",
    "vTotTrib": "totais_tributos_aproximado",
    "modFrete": "transporte_modalidade_frete",
    "placa": "transporte_veiculo_placa",
    "UF": "transporte_veiculo_uf",
    "RNTC": "transporte_veiculo_rntc",
    "placa": "transporte_reboque_placa",
    "UF": "transporte_reboque_uf",
    "RNTC": "transporte_reboque_rntc",
    "tPag": "tipo_pagamento",
    "vPag": "totais_icms_total_nota",
    "infAdFisco": "informacoes_adicionais_interesse_fisco",
    "infCpl": "informacoes_complementares_interesse_contribuinte",
}

mapaT = {
    "uf": "cUF",
    "codigo_numerico_aleatorio": "cNF",
    "natureza_operacao": "natOp",
    "modelo": "mod",
    "serie": "serie",
    "numero_nf": "nNF",
    "data_emissao": "dhEmi",
    "data_saida_entrada": "dhSaiEnt",
    "tipo_documento": "tpNF",
    "indicador_destino": "idDest",
    "municipio": "cMunFG",
    "tipo_impressao_danfe": "tpImp",
    "forma_emissao": "tpEmis",
    "dv_codigo_numerico_aleatorio": "cDV",
    "finalidade_emissao": "finNFe",
    "cliente_final": "indFinal",
    "indicador_presencial": "indPres",
    "indicador_intermediador": "indIntermed",
    "processo_emissao": "procEmi",
    "versao_processo_emissao": "verProc",
    "data_emissao": "dhCont",
    "totais_icms_base_calculo": "vBC",
    "totais_icms_total": "vICMS",
    "totais_icms_desonerado": "vICMSDeson",
    "totais_fcp_destino": "vFCPUFDest",
    "totais_icms_inter_destino": "vICMSUFDest",
    "totais_icms_remetente": "vICMSUFRemet",
    "totais_fcp": "vFCP",
    "totais_icms_st_base_calculo": "vBCST",
    "totais_icms_st_total": "vST",
    "totais_fcp_st": "vFCPST",
    "totais_fcp_st_ret": "vFCPSTRet",
    "totais_icms_total_produtos_e_servicos": "vProd",
    "totais_icms_total_frete": "vFrete",
    "totais_icms_total_seguro": "vSeg",
    "totais_icms_total_desconto": "vDesc",
    "totais_icms_total_ii": "vII",
    "totais_icms_total_ipi": "vIPI",
    "totais_icms_total_ipi_dev": "vIPIDevol",
    "totais_icms_pis": "vPIS",
    "totais_icms_cofins": "vCOFINS",
    "totais_icms_outras_despesas_acessorias": "vOutro",
    "totais_icms_total_nota": "vNF",
    "totais_tributos_aproximado": "vTotTrib",
    "transporte_modalidade_frete": "modFrete",
    "transporte_veiculo_placa": "placa",
    "transporte_veiculo_uf": "UF",
    "transporte_veiculo_rntc": "RNTC",
    "transporte_reboque_placa": "placa",
    "transporte_reboque_uf": "UF",
    "transporte_reboque_rntc": "RNTC",
    "tipo_pagamento": "tPag",
    "totais_icms_total_nota": "vPag",
    "informacoes_adicionais_interesse_fisco": "infAdFisco",
    "informacoes_complementares_interesse_contribuinte": "infCpl",
}

def NonnableDecimal(num):
    """retorna Decimal(num) se bool(num)==True, se não num"""
    return num and Decimal(num)

def mapProduto(nfe_dict:dict):
    nfe_produtos=nfe_dict['det']

    for prod in nfe_produtos:
        # IMPOSTOS
        nfe_icms = prod["imposto"]["ICMS"]["ICMS00"]
        icms = dict(
            icms_modalidade=nfe_icms.get('CST'),
            icms_aliquota=Decimal(nfe_icms.get('pICMS')),
            icms_valor=Decimal(nfe_icms.get('vICMS')),
            # fcp_base_calculo=Decimal(imposto.get('vBCFCP')),
            icms_st_percentual_reducao_bc=nfe_icms.get('pRedBCST'),
            # icms_st_valor_base_calculo=Decimal(imposto.get('vBCST')),
            icms_st_aliquota=nfe_icms.get('pICMSST'),
            # icms_st_valor=Decimal(imposto.get('vICMSST')),
            # fcp_st_base_calculo=Decimal(imposto.get('vBCFCPST')),
            icms_valor_base_calculo=Decimal(nfe_icms.get('vBC')),
            # icms_desonerado=Decimal(imposto.get('vICMSDeson')),
            icms_origem=nfe_icms.get('orig'),
            icms_modalidade_determinacao_bc=nfe_icms.get('modBC'),
            icms_st_modalidade_determinacao_bc=nfe_icms.get('modBCST')
        )

        nfe_ipi = prod["imposto"]["IPI"]

        ipi = dict(
            ipi_classe_enquadramento=nfe_ipi.get('cEnq'),
            ipi_codigo_enquadramento=nfe_ipi['IPINT'].get('CST')
        )

        nfe_confins = prod["imposto"]['COFINS']["COFINSOutr"]
        confins = dict(
            cofins_modalidade=nfe_confins.get('CST'),
            cofins_valor_base_calculo=Decimal(nfe_confins.get('vBC')),
            cofins_valor=Decimal(nfe_confins.get('vCOFINS')),
            cofins_aliquota_percentual=Decimal(nfe_confins.get('pCOFINS')),
        )

        nfe_pis = prod["imposto"]['PIS']["PISOutr"]
        pis = dict(

            pis_modalidade=nfe_pis["CST"],
            pis_valor_base_calculo=Decimal(nfe_pis["vBC"]),
            pis_aliquota_percentual=Decimal(nfe_pis["pPIS"]),
            pis_valor=Decimal(nfe_pis["vPIS"]),
        )

        produto = prod['prod']

        yield dict(
            codigo=produto.get("cProd"),
            ean=produto.get("cEAN"),
            descricao=produto.get("xProd"),
            ncm=produto.get("NCM"),
            cfop=produto.get("CFOP"),
            unidade_comercial=produto.get("uCom"),
            quantidade_comercial=produto.get("qCom"),
            valor_unitario_comercial=NonnableDecimal(produto.get("vUnCom")),
            valor_total_bruto=NonnableDecimal(produto.get("vProd")),
            ean_tributavel=produto.get("cEANTrib"),
            unidade_tributavel=produto.get("uTrib"),
            quantidade_tributavel=produto.get("qTrib"),
            valor_unitario_tributavel=NonnableDecimal(produto.get("vUnTrib")),
            ind_total=produto.get("indTot"),
            valor_tributos_aprox='',
            **pis,
            **icms,
            **ipi,
            **confins

        )

def mapEmitente(chave: str):
    if chave.startswith("endere"):
        return mapEndereco(chave)
    return {
        "cnpj": "CPF",
        "cnpj": "CNPJ",
        "razao_social": "xNome",
        "nome_fantasia": "xFant",
        "inscricao_estadual": "IE",
        "inscricao_estadual_subst_tributaria": "IEST",
        "inscricao_municipal": "IM",
        "cnae_fiscal": "CNAE",
        "codigo_de_regime_tributario": "CRT",
    }[chave]


def mapCliente(chave):
    if chave.startswith("endere"):
        return mapEndereco((chave))
    return {
        "razao_social": "xNome",
        "indicador_ie": "indIEDest",
        "inscricao_estadual": "IE",
        "inscricao_municipal": "IM",
        "email": "email",
        "inscricao_suframa": "ISUF",
    }[chave]


def mapEndereco(chave):
    return {
        "endereco_logradouro": "xLgr",
        "endereco_numero": "nro",
        "endereco_complemento": "xCpl",
        "endereco_bairro": "xBairro",
        "endereco_municipio": "xMun",
        "endereco_uf": "UF",
        "endereco_cep": "CEP",
        "endereco_pais": "cPais",
        "endereco_telefone": "fone",
        "endereco_cod_municipio": "cMun",  #: obter_codigo_por_municipio(,
        # 'xPais': obter_pais_por_codigo("endereco_pais"),
    }[chave]


def mapProdutoDEPREACATED(chave):
    nfe_chave = (
        {
            "codigo": "cProd",
            "ean": "cEAN",
            "descricao": "xProd",
            "ncm": "NCM",
            "cbenef": "cBenef",
            "cfop": "CFOP",
            "unidade_comercial": "uCom",
            "quantidade_comercialor": "qCom",
            "valor_unitario_comercial": "vUnCom",
            "valor_total_bruto": "vProd",
            "ean_tributavel": "cEANTrib",
            "unidade_tributavel": "uTrib",
            "quantidade_tributavel": "qTrib",
            "valor_unitario_tributavel": "vUnTrib",
            "total_frete": "vFrete",
            "total_seguro": "vSeg",
            "desconto": "vDesc",
            "outras_despesas_acessorias": "vOutro",
            "ind_total": "indTot",
            "numero_pedido": "xPed",
            "numero_item": "nItemPed",
            "nfci": "nFCI",
            "valor_tributos_aprox": "vTotTrib",
            "informacoes_adicionais": "infAdProd",
            "pdevol": "pDevol",
            "ipi_valor_ipi_dev": "vIPIDevol",
        }.get(chave)
        or _mapImposto(chave)
        or _mapICMS(chave)
        or _mapProdCombustive(chave)
        or _mapImpostoCofins(chave)
        or _mapImpostoPis(chave)
        or _mapImpostoIpi(chave)
    )
    if nfe_chave:
        open("n encontrado", "a").write(nfe_chave + "|")
        # raise Exception(f"{chave} não encontrada")
    return nfe_chave


def _mapProdCombustive(chave):
    return {
        "cProdANP": "cProdANP",
        "descANP": "descANP",
        "pGLP": "pGLP",
        "pGNn": "pGNn",
        "pGNi": "pGNi",
        "vPart": "vPart",
        "UFCons": "UFCons",
    }.get(chave)


def _mapImposto(chave):
    return {
        "imposto_importacao_valor_base_calculo": "vBC",
        "imposto_importacao_valor_despesas_aduaneiras": "vDespAdu",
        "imposto_importacao_valor": "vII",
        "imposto_importacao_valor_iof": "vIOF",
    }.get(chave)


def _mapICMS(chave):
    return {
        "icms_modalidade": "CST",
        "icms_aliquota": "pICMS",
        "icms_valor": "vICMS",
        "fcp_percentual": "pFCP",
        "fcp_valor": "vFCP",
        "icms_modalidade": "CST",
        "icms_aliquota": "pICMS",
        "icms_valor": "vICMS",
        "fcp_base_calculo": "vBCFCP",
        "fcp_percentual": "pFCP",
        "fcp_valor": "vFCP",
        "icms_st_percentual_adicional": "pMVAST",
        "icms_st_percentual_reducao_bc": "pRedBCST",
        "icms_st_valor_base_calculo": "vBCST",
        "icms_st_aliquota": "pICMSST",
        "icms_st_valor": "vICMSST",
        "fcp_st_base_calculo": "vBCFCPST",
        "fcp_st_percentual": "pFCPST",
        "fcp_st_valor": "vFCPST",
        "icms_modalidade": "CST",
        "icms_percentual_reducao_bc": "pRedBC",
        "icms_valor_base_calculo": "vBC",
        "icms_aliquota": "pICMS",
        "icms_valor": "vICMS",
        "fcp_base_calculo": "vBCFCP",
        "fcp_percentual": "pFCP",
        "fcp_valor": "vFCP",
        "icms_desonerado": "vICMSDeson",
        "icms_modalidade": "CST",
        "icms_st_percentual_adicional": "pMVAST",
        "icms_st_percentual_reducao_bc": "pRedBCST",
        "icms_st_valor_base_calculo": "vBCST",
        "icms_st_aliquota": "pICMSST",
        "icms_st_valor": "vICMSST",
        "fcp_st_base_calculo": "vBCFCPST",
        "fcp_st_percentual": "pFCPST",
        "fcp_st_valor": "vFCPST",
        "icms_desonerado": "vICMSDeson",
        "icms_desonerado": "vICMSDeson",
        "fcp_base_calculo": "vBCFCP",
        "fcp_percentual": "pFCP",
        "fcp_valor": "vFCP",
        "fcp_st_base_calculo": "vBCFCPSTRet",
        "fcp_st_percentual": "pFCPSTRet",
        "fcp_st_valor": "vFCPSTRet",
        "icms_percentual_reducao_bc": "pRedBC",
        "icms_valor_base_calculo": "vBC",
        "icms_aliquota": "pICMS",
        "icms_valor": "vICMS",
        "fcp_base_calculo": "vBCFCP",
        "fcp_percentual": "pFCP",
        "fcp_valor": "vFCP",
        "icms_st_percentual_adicional": "pMVAST",
        "icms_st_percentual_reducao_bc": "pRedBCST",
        "icms_st_valor_base_calculo": "vBCST",
        "icms_st_aliquota": "pICMSST",
        "icms_st_valor": "vICMSST",
        "fcp_st_base_calculo": "vBCFCPST",
        "fcp_st_percentual": "pFCPST",
        "fcp_st_valor": "vFCPST",
        "icms_desonerado": "vICMSDeson",
        "icms_valor_base_calculo": "vBC",
        "icms_percentual_reducao_bc": "pRedBC",
        "icms_aliquota": "pICMS",
        "icms_valor": "vICMS",
        "fcp_base_calculo": "vBCFCP",
        "fcp_percentual": "pFCP",
        "fcp_valor": "vFCP",
        "icms_st_percentual_adicional": "pMVAST",
        "icms_st_percentual_reducao_bc": "pRedBCST",
        "icms_st_valor_base_calculo": "vBCST",
        "icms_st_aliquota": "pICMSST",
        "icms_st_valor": "vICMSST",
        "fcp_st_base_calculo": "vBCFCPST",
        "fcp_st_percentual": "pFCPST",
        "fcp_st_valor": "vFCPST",
        "icms_desonerado": "vICMSDeson",
        "icms_csosn": "CSOSN",
        "icms_csosn": "CSOSN",
        "icms_csosn": "CSOSN",
        "icms_st_percentual_adicional": "pMVAST",
        "icms_st_percentual_reducao_bc": "pRedBCST",
        "icms_st_valor_base_calculo": "vBCST",
        "icms_st_aliquota": "pICMSST",
        "icms_st_valor": "vICMSST",
        "fcp_st_base_calculo": "vBCFCPST",
        "fcp_st_percentual": "pFCPST",
        "fcp_st_valor": "vFCPST",
        "icms_csosn": "CSOSN",
        "icms_csosn": "CSOSN",
        "icms_valor_base_calculo": "vBC",
        "icms_percentual_reducao_bc": "pRedBC",
        "icms_aliquota": "pICMS",
        "icms_valor": "vICMS",
        "icms_st_percentual_adicional": "pMVAST",
        "icms_st_percentual_reducao_bc": "pRedBCST",
        "icms_st_valor_base_calculo": "vBCST",
        "icms_st_aliquota": "pICMSST",
        "icms_st_valor": "vICMSST",
        "fcp_st_base_calculo": "vBCFCPST",
        "fcp_st_percentual": "pFCPST",
        "fcp_st_valor": "vFCPST",
        "icms_origem": "orig",
        "icms_modalidade_determinacao_bc": "modBC",
        "icms_valor_base_calculo": "vBC",
        "icms_origem": "orig",
        "icms_st_modalidade_determinacao_bc": "modBCST",
        "icms_origem": "orig",
        "icms_modalidade_determinacao_bc": "modBC",
        "icms_motivo_desoneracao": "motDesICMS",
        "icms_origem": "orig",
        "icms_st_modalidade_determinacao_bc": "modBCST",
        "icms_motivo_desoneracao": "motDesICMS",
        "icms_origem": "orig",
        "icms_modalidade": "CST",
        "icms_motivo_desoneracao": "motDesICMS",
        "icms_origem": "orig",
        "icms_modalidade_determinacao_bc": "modBC",
        "icms_origem": "orig",
        "icms_origem": "orig",
        "icms_modalidade_determinacao_bc": "modBC",
        "icms_st_modalidade_determinacao_bc": "modBCST",
        "icms_motivo_desoneracao": "motDesICMS",
        "icms_origem": "orig",
        "icms_modalidade_determinacao_bc": "modBC",
        "icms_st_modalidade_determinacao_bc": "modBCST",
        "icms_motivo_desoneracao": "motDesICMS",
        "icms_origem": "orig",
        "icms_aliquota": "pCredSN",
        "icms_credito": "vCredICMSSN",
        "icms_origem": "orig",
        "icms_origem": "orig",
        "icms_st_modalidade_determinacao_bc": "modBCST",
        "icms_aliquota": "pCredSN",
        "icms_credito": "vCredICMSSN",
        "icms_origem": "orig",
        "icms_origem": "orig",
        "icms_modalidade_determinacao_bc": "modBC",
        "icms_st_modalidade_determinacao_bc": "modBCST",
        "icms_aliquota": "pCredSN",
        "icms_credito": "vCredICMSSN",
    }.get(chave)


def _mapImpostoCofins(chave):
    return {
        "cofins_modalidade": "CST",
        "cofins_modalidade": "CST",
        "cofins_valor_base_calculo": "vBC",
        "cofins_aliquota_percentual": "pCOFINS",
        "cofins_valor": "vCOFINS",
        "cofins_modalidade": "CST",
        "quantidade_comercial": "qBCProd",
        "cofins_aliquota_reais": "vAliqProd",
        "cofins_valor": "vCOFINS",
        "cofins_modalidade": "CST",
        "quantidade_comercial": "qBCProd",
        "cofins_aliquota_reais": "vAliqProd",
        "cofins_valor_base_calculo": "vBC",
        "cofins_aliquota_percentual": "pCOFINS",
        "cofins_valor": "vCOFINS",
    }.get(chave)


def _mapImpostoPis(chave):
    return {
        "pis_modalidade": "CST",
        "pis_modalidade": "CST",
        "pis_valor_base_calculo": "vBC",
        "pis_aliquota_percentual": "pPIS",
        "pis_valor": "vPIS",
        "pis_modalidade": "CST",
        "quantidade_comercial": "qBCProd",
        "pis_aliquota_reais": "vAliqProd",
        "pis_valor": "vPIS",
        "pis_modalidade": "CST",
        "quantidade_comercial": "qBCProd",
        "pis_aliquota_reais": "vAliqProd",
        "pis_valor_base_calculo": "vBC",
        "pis_aliquota_percentual": "pPIS",
        "pis_valor": "vPIS",
    }.get(chave)

def _mapImpostoIpi(chave):
    return {
        "ipi_classe_enquadramento":'cEnq' ,
"ipi_codigo_enquadramento":'CST' 
    }.get(chave)