from ipvh_srv import send_command
from globals import logger


logger.escrever("[kill_ipvh_srv.py] Enviando comando de finalização do servidor IPVH")
try:
    send_command('exit')
except:
    logger.escrever("[kill_ipvh_srv.py] Não foi possível mater o servidor de dados")
