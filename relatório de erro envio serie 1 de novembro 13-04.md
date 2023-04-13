Complementares = 1312.py 2624.total # versão .py das notas geradas pelo Leo, antes de enviar pro pynfe
Dicts originais = 1313 # versão .py das notas originais geradas pelo Leo
notagerada = 1312 # registro da nota gerada logo antes da request de autorização
enviadas (envio[2] e envio[1]) = 405 # nota e recibo logo após a request da autorização
consultas = 207 # resultado das consultas de recibos, ou seja, logo aṕos request de consulta

notagerada - enviadas = 907

erro_autorização logado = 907 (bate com notagerada - enviadas(com recibo))
erro_consulta = 198 (bate com enviadas - consultas)

pelo log:
    Originais carregadas = 1917
    Originais ignoradas = 604
    Originais processadas/em processamento = 1313

Eu acho que o programa travou quando ia processar a nota 1313, logo depois de adicionar os produtos,
porque o log termina com:
"[...]
```log
2023-04-13T11:19:16.040827: Aberto Original ../../Downloads/enviando_nfes_complementares/novembro/MES 11 SERIE 2/35221146364058000115550020000190221960378928-nfe.xml 
2023-04-13T11:19:16.042304: Aberto template NFS/Base/base.xml
2023-04-13T11:19:16.056327: Adicionando produtos
2023-04-13T11:19:16.056744: [WARNING] nota original 35221146364058000115550020000190221960378928 teve sua complementar associada à serie 46184
2023-04-13T11:19:16.057191: Produto adicionado: {...}
2023-04-13T11:19:16.057297: Produtos adicionados!```"


em suma,
- no processo principal:
    processou 1312 notas, travou na 1313
- nos processos filhos: 
    pynfe gerou 1312
    falharam na autorização 907
    foram enviadas para autorização 405
    falharam 198 consultas dos 405 recibos
    recibos consultados 207 - todos autorizados
sabemos de 207 notas autorizadas
agora vou verificar os recibos restantes
depois vou ver qual última nota que gerou recibo, olhar a proxima e ver se ela existe
se não, vou enviar dela pra frente