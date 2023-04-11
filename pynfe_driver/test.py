# import nfe_as_dict
import nfe_as_dict2
import pynfe_driver as pynd

pynd.configura(
    "/home/dev/nfs_transform/NFS/certificados/CERTIFICADO LUZ LED COMERCIO ONLINE_VENCE 13.05.2023.p12",
    "123456",
    False
)

# xml_assinado = pynd.converte_para_pynfe_XML_assinado(
#     nfe_as_dict.nfe_dict
# )
# xml_assinado2 = pynd.converte_para_pynfe_XML_assinado(
#     nfe_as_dict2.nfe_dict
# )

pynd.consulta(
    '35221146364058000115550020000143971529646913'
)
