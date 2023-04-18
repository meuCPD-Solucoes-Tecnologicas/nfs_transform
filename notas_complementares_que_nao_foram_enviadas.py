# pegando originais

# arir a pasta "log_erro"
# abrir arrquivo notas_complementares_que_nao_foram_enviadas.txt
# para cada linha do arquivo, que é um id, abrir a nota complementar em log_erro.py
# pegar o nferef dessa nota e salvar em um arquivo notas_nao_enviadas.txt

import os

geradas = []
nfes_comepelementares = []
log_erros = os.listdir("log_erro")

with open("notas_complementares_que_nao_foram_enviadas.txt", "r") as arquivo:
    for linha in arquivo:
        id = linha.strip()
        geradas.append(id)
        nfes_comepelementares.append(
            "log_erro/"+next(filter(lambda f: f.startswith(f"{id}notagerada"), log_erros))
        )
# abrir a pasta log_erro e pgar arquivos com nome tipo f'{id}notagerada*.xml'
# 35230446364058000115550020000448721384911297notagerada_2023-04-13T10:54:23:172297.xml
#     arquivo_nfe for arquivo_nfe in  if arquivo_nfe.startswith(f'{id}notagerada')
# ]
for nfe in sorted(nfes_comepelementares):
    with open(nfe, "r") as arquivo, open("notas_nao_enviadas.txt", "a") as originais:
        # pegar informação da tag <refNFe>35221146364058000115550020000143891995080006</refNFe>
        refNfe = arquivo.read().split("<refNFe>")[1].split("</refNFe>")[0]
        originais.write(refNfe + "\n")
