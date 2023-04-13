import os
from progress.bar import Bar


files = os.listdir('./')
bar = Bar('Processing', max=len(files))

msg_homologacao = "Rejeição: Chave de Acesso referenciada inexistente [nRef: 1]"
msg_producao = "Autorizado o uso da NF-e"

with open('falharam','a') as fdf:
    for file in files:
        if not file.endswith('.xml'):
            continue
        with open(file) as fd:
            try:
                conteudo = fd.read()
                if conteudo.find(msg_producao)==-1:
                    motivo = conteudo[conteudo.find('<xMotivo>')+9:conteudo.find('</xMotivo>')]
                    fdf.write(f'{file}\nmotivo: {motivo}\n\n')
            except UnicodeDecodeError as ue:
                print(ue)
                print(file)
                __import__('ipdb').set_trace()
                print()
        bar.next()

bar.finish()