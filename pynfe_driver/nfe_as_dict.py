from pprint import pp
from typing import Dict, TypedDict


nfe_xml = {
    "@versao": "4.00",
    "ide": {
        "cUF": "35",
        "cNF": "69838101",
        "natOp": "Complementar de ICMS (Serie 1)",
        "mod": "55",
        "serie": "1",
        "nNF": "2708",
        "dhEmi": "2023-04-03T16:27:02-03:00",
        "tpNF": "1",
        "idDest": "2",
        "cMunFG": "3543907",
        "tpImp": "1",
        "tpEmis": "1",
        "cDV": "4",
        "tpAmb": "1",
        "finNFe": "2",
        "indFinal": "1",
        "indPres": "2",
        "procEmi": "0",
        "verProc": "Tiny ERP",
        "NFref": {"refNFe": "35220846364058000115550010000001161698381017"},
    },
    "emit": {
        "CNPJ": "46364058000115",
        "xNome": "LUZ LED COMERCIO ONLINE LTDA",
        "xFant": "LUZ LED DECOR",
        "enderEmit": {
            "xLgr": "Rua 7",
            "nro": "192",
            "xBairro": "Zona Central",
            "cMun": "3543907",
            "xMun": "Rio Claro",
            "UF": "SP",
            "CEP": "13500143",
            "cPais": "1058",
            "xPais": "Brasil",
            "fone": "1935571411",
        },
        "IE": "587462103112",
        "CRT": "3",
    },
    "dest": {
        "CPF": "61070980030",
        "xNome": "Flavio Martins",
        "enderDest": {
            "xLgr": "Rivaldo Azambuja Guimaraes",
            "nro": "033",
            "xBairro": "centro",
            "cMun": "4321303",
            "xMun": "Taquari",
            "UF": "RS",
            "CEP": "95860000",
            "cPais": "1058",
            "xPais": "Brasil",
        },
        "indIEDest": "9",
    },
    "det": {
        "@nItem": "1",
        "prod": {
            "cProd": "CFOP6106",
            "cEAN": "SEM GTIN",
            "xProd": "COMPLEMENTO DE ICMS",
            "NCM": "94053100",
            "CFOP": "6108",
            "uCom": "UN",
            "qCom": "1.0000",
            "vUnCom": "0.00",
            "vProd": "0.00",
            "cEANTrib": "SEM GTIN",
            "uTrib": "UN",
            "qTrib": "1.0000",
            "vUnTrib": "0.00",
            "indTot": "1",
        },
        "imposto": {
            "ICMS": {
                "ICMS00": {
                    "orig": "2",
                    "CST": "00",
                    "modBC": "1",
                    "vBC": "159.90",
                    "pICMS": "4.00",
                    "vICMS": "6.40",
                }
            },
            "IPI": {"cEnq": "999", "IPINT": {"CST": "53"}},
            "PIS": {
                "PISOutr": {
                    "CST": "49",
                    "vBC": "0.00",
                    "pPIS": "0.00",
                    "vPIS": "0.00",
                }
            },
            "COFINS": {
                "COFINSOutr": {
                    "CST": "49",
                    "vBC": "0.00",
                    "pCOFINS": "0.00",
                    "vCOFINS": "0.00",
                }
            },
        },
    },
    "total": {
        "ICMSTot": {
            "vBC": "159.90",
            "vICMS": "6.40",
            "vICMSDeson": "0.00",
            "vFCPUFDest": "0.00",
            "vICMSUFDest": "0.00",
            "vICMSUFRemet": "0.00",
            "vFCP": "0.00",
            "vBCST": "0.00",
            "vST": "0.00",
            "vFCPST": "0.00",
            "vFCPSTRet": "0.00",
            "vProd": "0.00",
            "vFrete": "0.00",
            "vSeg": "0.00",
            "vDesc": "0.00",
            "vII": "0.00",
            "vIPI": "0.00",
            "vIPIDevol": "0.00",
            "vPIS": "0.00",
            "vCOFINS": "0.00",
            "vOutro": "0.00",
            "vNF": "0.00",
        }
    },
    "transp": {"modFrete": "9", "vol": {"pesoL": "0.000", "pesoB": "0.000"}},
    "pag": {"detPag": {"tPag": "90", "vPag": "0"}},
    "infAdic": {
        "infCpl": 'Conforme artigo 182 IV do RICMS, Nota fiscal complementar de ICMS referente a NF "*116*" da serie "*01*" de "*31/08/2022*".'
    },
    "infRespTec": {
        "CNPJ": "15088992000128",
        "xContato": "Fernando",
        "email": "integracao@tiny.com.br",
        "fone": "05430558200",
    },
}


