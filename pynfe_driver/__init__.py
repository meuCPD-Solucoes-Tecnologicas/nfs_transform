from .driver import (
    converte_para_pynfe_XML_assinado,
    configura,
    autorização,
    consulta_recibo,
    consulta,
    inutilizacao,
    evento_cancelamento
)
import os

os.makedirs("log", exist_ok=True)
