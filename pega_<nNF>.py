import os

recibos = [recibo for recibo in os.listdir("enviadas") if "envio[2]" in recibo]

#pega <nNF>1234</nNF> do arquivo
nnfs =[]
for recibo in recibos:
    with open(f'enviadas/{recibo}', 'r') as f:
        conteudo = f.read()
        nNF = conteudo[conteudo.find("<nNF>") + 5: conteudo.find("</nNF>")]
        nnfs.append(int(nNF))
with open('nNFs','a') as f2:
    f2.write('\n'.join(map(str,sorted(nnfs))))