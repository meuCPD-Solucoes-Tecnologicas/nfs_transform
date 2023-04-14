from multiprocessing import Process
import os
from time import sleep
import pynfe_driver

pynfe_driver.configura(
    caminho_certificado="/home/dev/notas_hell/nfs_transform/NFS/certificados/LUZ_LED_NOVO.pfx",
    senha_certificado="123456",
    ambiente_homologacao=False,
    # ignora_homologacao_warning=True,
    uf="SP",
    gera_log=True,
)

recibos = [recibo for recibo in os.listdir("enviadas") if "envio[1]" in recibo]




pynfe_driver.consulta_recibo('351011112297145', '35230446364058000115550020000460681436179080')

breakpoint()
lista_precessos = []
consutadas = 0
for recibo in recibos:
    # exemplo nome arquivo = 35230446364058000115550020000460681436179080envio[1]_2023-04-13T11:18:57:706420.xml
    
    pos_chave_recibo = recibo.find("<nRec>") + 6
    chave_recibo = recibo[pos_chave_recibo : pos_chave_recibo + 15]
    chave_acesso = ''
    __import__('ipdb').set_trace()
    lista_precessos.append(
        Process(
        target=pynfe_driver.consulta_recibo,
        args=(chave_recibo, chave_acesso),
        )
    )
    if len(lista_precessos)>=10:
        for processo in lista_precessos:
            processo.start()
            breakpoint()
        try:
            while processo := lista_precessos.pop():
                processo.join()
        except IndexError:
            consutadas +=10
            print(f'{consutadas} processos finalizados')
        sleep(10)

if len(lista_precessos)>0:
    for processo in lista_precessos:
        processo.start()
    try:
        while processo := lista_precessos.pop():
            processo.join()
    except IndexError:
        print('todos processos finalizados')