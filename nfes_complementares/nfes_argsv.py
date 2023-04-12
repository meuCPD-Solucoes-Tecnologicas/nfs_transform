import argparse

parser = argparse.ArgumentParser(description="Script para gerar nfs complementares")
parser.add_argument(
    "-o",
    "--pasta_origem",
    help="Pasta onde estão as nfes originais a serem complementadas",
    required=True,
)
parser.add_argument(
    "-g",
    "--pasta_geradas",
    help="Pasta para guardar nfes complementares geradas/enviadas",
    default="./geradas",
)
parser.add_argument(
    "-r", "--pasta_recibos", help="Pasta para os recibos", default="./recibos"
)
parser.add_argument(
    "-cr",
    "--pasta_consultas_recibos",
    help="Pasta para o resultado dos recibos consultados",
    default="./consultas_recibos",
)
parser.add_argument('-certificado', '--caminho-certificado', help='Caminho para o certificado', required=True)
parser.add_argument('-senha', '--senha-certificado', help='Senha do certificado', required=True)
parser.add_argument("-plog", "--pasta_log", help="Pasta para o log", default="./log")
parser.add_argument("--envio-producao", action="store_true", help="Envia para produção")
# parse.add_argument('--envio-homologacao', action='store_true', help='Envia para homologação')
parser.add_argument(
    "-start_s1", "--start_serie_1", help="Número nNF de início da série 1", default=0
)
parser.add_argument(
    "-start_s2", "--start_serie_2", help="Número nNF de início da série 2", default=0
)

# args = None
args = parser.parse_args()
# def init_args():
#     global args