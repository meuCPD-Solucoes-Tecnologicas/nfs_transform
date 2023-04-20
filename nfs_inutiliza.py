from multiprocessing import Process
import os
import pynfe_driver

raise NotImplemented("Inutilização de NF-e não finalizada")


pynfe_driver.configura(
    caminho_certificado="/home/dev/notas_hell/nfs_transform/NFS/certificados/CERTIFICADO LUZ LED COMERCIO ONLINE_VENCE 13.05.2023.p12",
    senha_certificado="123456",
    ambiente_homologacao=True,
    # ignora_homologacao_warning=True,
    uf="SP",
    gera_log=True,
)

nnf_inicial = 46184
nnf_final = 46589
justificativa = "Notas emitidas em duplicidade por erro do sistema."
cnpj="46364058000115"
serie = 2


pynfe_driver.inutilizacao(
    modelo='nfe',
    cnpj=cnpj,
    numero_inicial=nnf_inicial,
    numero_final=nnf_final,
    justificativa=justificativa,
    serie=serie
)