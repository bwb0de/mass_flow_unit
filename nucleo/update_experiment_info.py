from ipvh_srv import send_command
from globals import logger

logger.escrever("[update_experiment_info.py] Enviando comando para atualização informações do pesquisador em IPVH")
try:
    send_command('update_exp')
except:
    logger.escrever("[update_experiment_info.py] Não foi possível atualizar dados, IPVH em execução?")


