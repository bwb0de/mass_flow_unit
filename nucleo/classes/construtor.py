import pandas as pd
from matplotlib import pyplot as  plt

class ConstrutorGrafico:
    def __init__(self) -> None:
        self.valores_primarios = [0.0] * 100
        self.valores_secundarios = [0.0] * 100
        self.range_100 = tuple(range(100))

    def gerar_grafico(self, sensor, valores_lcr):

        for primarios, secundarios in valores_lcr:
            self.valores_primarios.append(primarios)
            self.valores_secundarios.append(secundarios)

        i = 0
        while len(self.valores_primarios[i:]) > 100:
            i += 1
        
        self.valores_primarios = self.valores_primarios[i:]
        self.valores_secundarios = self.valores_secundarios[i:]

        fig, ax = plt.subplots()

        ax.plot(self.range_100, self.valores_primarios, label='Primary', color='blue')
        ax.plot(self.range_100, self.valores_secundarios, label='Secondary', color='red')
        
        ax.fill_between(self.range_100, self.valores_primarios, color='blue', alpha=0.2)
        ax.fill_between(self.range_100, self.valores_secundarios, color='red', alpha=0.2)
        
        ax.set_title(sensor, fontsize=20)
        
        fig.savefig(f'C:\\Users\\Daniel Cruz\\Documents\\Devel\\python\\mass_flow_unit\\static\\img\\{sensor}.png')
        plt.close()

        return f'/static/img/{sensor}.png'
