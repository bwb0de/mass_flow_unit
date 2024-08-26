import time
from mass_flow_unit import MassFlowUnit
from multiprocessing import Process

taxa_de_transmissao = 9600

mass_flow_unit1 = MassFlowUnit('COM5', taxa_de_transmissao)
mass_flow_unit2 = MassFlowUnit('COM6', taxa_de_transmissao)
mass_flow_unit3 = MassFlowUnit('COM7', taxa_de_transmissao)
mass_flow_unit4 = MassFlowUnit('COM8', taxa_de_transmissao)


print(mass_flow_unit1.fluxo_maximo)
print(mass_flow_unit1.fracao_de_fluxo)
print(mass_flow_unit1.porta_de_conexao)
print(mass_flow_unit1.conteudo_fluxo)

print('')
print(mass_flow_unit2.fluxo_maximo)
print(mass_flow_unit2.fracao_de_fluxo)
print(mass_flow_unit2.porta_de_conexao)
print(mass_flow_unit2.conteudo_fluxo)

print('')
print(mass_flow_unit3.fluxo_maximo)
print(mass_flow_unit3.fracao_de_fluxo)
print(mass_flow_unit3.porta_de_conexao)
print(mass_flow_unit3.conteudo_fluxo)

print('')
print(mass_flow_unit4.fluxo_maximo)
print(mass_flow_unit4.fracao_de_fluxo)
print(mass_flow_unit4.porta_de_conexao)
print(mass_flow_unit4.conteudo_fluxo)




'''
for abertura, tempo in parametros_abertura_tempo:
    print(mass_flow_unit1.enviar_comandos(['DI', 'PI','M,D', f'SP,{abertura}', 'SP', 'V,M,A']))
    print(mass_flow_unit2.enviar_comandos(['DI', 'PI','M,D', f'SP,{abertura}', 'SP', 'V,M,A']))
    print(mass_flow_unit3.enviar_comandos(['DI', 'PI','M,D', f'SP,{abertura}', 'SP', 'V,M,A']))
    print(mass_flow_unit4.enviar_comandos(['DI', 'PI','M,D', f'SP,{abertura}', 'SP', 'V,M,A']))
    time.sleep(tempo)

'''