from mass_flow_unit import MassFlowUnit, MassFlowUnitTest
from mass_flow_orquestrator_parallel import Orquestrador


def inicializar_orquestrador():
    taxa_de_transmissao = 9600
    #mass_flow_unit1 = MassFlowUnitTest('COM5', taxa_de_transmissao, 200, 'Ar')
    #mass_flow_unit2 = MassFlowUnitTest('COM6', taxa_de_transmissao, 200, 'Ar')
    #mass_flow_unit3 = MassFlowUnitTest('COM7', taxa_de_transmissao, 100, 'produto')
    #mass_flow_unit4 = MassFlowUnitTest('COM8', taxa_de_transmissao, 100, 'produto')    
    mass_flow_unit1 = MassFlowUnit('COM5', taxa_de_transmissao, 100, 'produto')
    mass_flow_unit2 = MassFlowUnit('COM6', taxa_de_transmissao, 200, 'Ar')
    mass_flow_unit3 = MassFlowUnit('COM7', taxa_de_transmissao, 100, 'produto')
    mass_flow_unit4 = MassFlowUnit('COM8', taxa_de_transmissao, 200, 'Ar')
    o1 = Orquestrador([mass_flow_unit1, mass_flow_unit2, mass_flow_unit3, mass_flow_unit4], exp_max_flow=400)
    return o1



