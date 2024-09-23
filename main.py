import os 
import json

from flask import jsonify, Flask
from flask import render_template, request, redirect

from nucleo.mass_flow_setup import inicializar_orquestrador_mass_flow
from nucleo.mass_flow_info_reader import update_info

from nucleo.paths import root, parametros

os.chdir(root)

### Variáveis globais
em_execucao = False
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/api/run')
def mass_flow_run():
    global em_execucao, orq_mass_flow
    em_execucao = True
    lista_fluxo_nao_ar_tempo = None
    with open(parametros, 'r') as arquivo_parametros:
        lista_fluxo_nao_ar_tempo = json.loads(arquivo_parametros.read())
    orq_mass_flow = inicializar_orquestrador_mass_flow()
    orq_mass_flow.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)
    orq_mass_flow.executar_rotina()
    return jsonify("Procedimento iniciado...")



@app.route('/api/stop')
def mass_flow_stop():
    global em_execucao, orq_mass_flow
    em_execucao = False
    orq_mass_flow.interromper()
    return jsonify("Procedimento interrompido...")



@app.route('/api/equipo')
def mass_flow_equipo():
    return jsonify(orq_mass_flow.status_equipamentos())



@app.route('/api/check')
def mass_flow_check():
    if not em_execucao:
        return jsonify("Não há o que checar, procedimentos não estão em execução...")
    return jsonify(update_info())



@app.route('/rotina_experimental', methods=['GET', 'POST'])
def formulario_exp():
    if request.method == 'POST':
        with open(parametros, 'w') as params_file:
            dados = request.form['acumulador_de_parametros'].strip('[[').strip(']]').strip('"').replace('","',',').split("],[")
            dados_convertidos = [fluxo_tempo.replace('"',"").split(',') for fluxo_tempo in dados]
            dados_convertidos = [(float(fluxo), int(tempo)) for fluxo, tempo in dados_convertidos]
            json.dump(dados_convertidos, params_file, indent=4)

        return redirect('/')
    
    with open(parametros, 'r') as params_file:
        params = json.loads(params_file.read())

    return render_template('formulario_rotina.html', params=params)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





