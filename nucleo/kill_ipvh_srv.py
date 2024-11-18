from ipvh_srv import send_command

try:
    send_command('exit')
    print('Matando servidor de dados...')
except:
    print('Não foi possível matar servidor de dados...')    