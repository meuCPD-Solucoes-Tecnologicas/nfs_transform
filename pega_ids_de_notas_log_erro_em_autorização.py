# abri a pasta log_erro e pega todos os arquivos que começa com erro_autoriz
import glob


arquivos = glob.glob('log_erro/erro_autoriz*.xml')
with open('notas_complementares_que_nao_sabemos_se_enviou','a') as f:
    # log_erro/erro_autorizacao35230446364058000115550020000457281283461777_2023-04-13T10:56:31:810693.xml
    #25+44=
    __import__('ipdb').set_trace()
    f.write(
        '\n'.join([_[25:69] for _ in arquivos])
    )
