import os
import pandas as pd
import json


pasta_dados_experimento = "C:\\Users\\Mauro\\Desktop\\Dados Experimentos"
arquivo_dados_experimento = "C:\\Users\\Mauro\\Documents\\Devel\\mass_flow_unit\\config\\experimento.json"

production_root = 'C:\\Users\\Mauro\\Documents\\Devel\\mass_flow_unit'
development_root1 = 'C:\\Users\\Daniel Cruz\\Documents\\Devel\\python\\mass_flow_unit'
development_root2 = '/home/danielc/Documentos/Devel/GitHub/mass_flow_unit'
root = production_root

experimento_ultimos_parametros_windows = f"{root}\\config\\experimento_ultimos_parametros_tempo.txt"
experimento_ultimos_parametros_linux = f"{root}/config/experimento_ultimos_parametros_tempo.txt"
experimento_ultimos_parametros = experimento_ultimos_parametros_windows




with open(experimento_ultimos_parametros, 'r') as dados_experimento_ultimos_par:
    folder = dados_experimento_ultimos_par.read()
    arquivo_dados_alvo = folder.replace("\\", "\\\\")+'\\dados_sensores.json'

with open(arquivo_dados_alvo, 'r') as arquivo_dados:
    dados = json.loads(arquivo_dados.read())

S1_primary = dados['sensor_loop']['S1']['primary'],
S1_secundary = dados['sensor_loop']['S1']['secondary'],
S2_primary = dados['sensor_loop']['S2']['primary'],
S2_secundary = dados['sensor_loop']['S2']['secondary'],
S3_primary = dados['sensor_loop']['S3']['primary'],
S3_secundary = dados['sensor_loop']['S3']['secondary'],
S4_primary = dados['sensor_loop']['S4']['primary'],
S4_secundary = dados['sensor_loop']['S4']['secondary'],
S5_primary = dados['sensor_loop']['S5']['primary'],
S5_secundary = dados['sensor_loop']['S5']['secondary'],
S6_primary = dados['sensor_loop']['S6']['primary'],
S6_secundary = dados['sensor_loop']['S6']['secondary'],
S7_primary = dados['sensor_loop']['S7']['primary'],
S7_secundary = dados['sensor_loop']['S7']['secondary'],
S8_primary = dados['sensor_loop']['S8']['primary'],
S8_secundary = dados['sensor_loop']['S8']['secondary']

export_data = [
    S1_primary,
    S1_secundary,
    S2_primary,
    S2_secundary,
    S3_primary,
    S3_secundary,
    S4_primary,
    S4_secundary,
    S5_primary,
    S5_secundary,
    S6_primary,
    S6_secundary,
    S7_primary,
    S7_secundary,
    S8_primary,
    S8_secundary 
]


min_len = 1000000

for col in export_data[:]:
    if col == export_data[-1]:
        current_len = len(col)
        if current_len < min_len:
            min_len = current_len
        break
    current_len = len(col[0])
    if current_len < min_len:
        min_len = current_len    

export_data_formated = []

for idx, col in enumerate(export_data[:]):
    
    if col == export_data[-1]:
        current_len = len(col)
        if current_len > min_len:
            export_data[idx] = col[0:min_len]
            export_data_formated.append(col[0:min_len])
        else:
            export_data_formated.append(col[:])
            #print(col[0:min_len-1], '***')
        break
    current_len = len(col[0])
    if current_len > min_len:
        export_data[idx] = col[0][0:min_len]
        export_data_formated.append(col[0][0:min_len])
    else:
        export_data_formated.append(col[0][:])
        
        
      

colunas_dataframe = {
    'S1_primary': export_data_formated[0],
    'S1_secundary': export_data_formated[1],
    'S2_primary': export_data_formated[2],
    'S2_secundary': export_data_formated[3],
    'S3_primary': export_data_formated[4],
    'S3_secundary': export_data_formated[5],
    'S4_primary': export_data_formated[6],
    'S4_secundary': export_data_formated[7],
    'S5_primary': export_data_formated[8],
    'S5_secundary': export_data_formated[9],
    'S6_primary': export_data_formated[10],
    'S6_secundary': export_data_formated[11],
    'S7_primary': export_data_formated[12],
    'S7_secundary': export_data_formated[13],
    'S8_primary': export_data_formated[14],
    'S8_secundary': export_data_formated[15]
}

df = pd.DataFrame(colunas_dataframe)
df.to_excel(folder+'\\dados_tabelados.xlsx', index=False)

