import random
import os 
import json
import pandas as pd
import matplotlib.pyplot as plt

from flask import jsonify, Flask
from flask import render_template, request, redirect

from nucleo.orquestrator_setup import inicializar_orquestrador_mass_flow, inicializar_orquestrador_mass_flow_teste
from nucleo.mass_flow_info_reader import update_info

from nucleo.paths import root, parametros_mass_flow, arduino_config, lcr_config

os.chdir(root)

### Variáveis globais
em_execucao = False

s0 = []
s1 = []
s2 = []
s3 = []
s4 = []
s5 = []
s6 = []
s7 = []


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/monitor')
def monitor():
    return render_template('monitor.html')



@app.route('/api/monitor')
def monitor_api():
    images = []
    for i in range(8):
        images.append(f'/static/img/S{i}.png')
    return jsonify({'images': images})





@app.route('/api/run')
def mass_flow_run():
    global em_execucao, orq_mass_flow
    em_execucao = True
    lista_fluxo_nao_ar_tempo = None
    with open(parametros_mass_flow, 'r') as arquivo_parametros:
        lista_fluxo_nao_ar_tempo = json.loads(arquivo_parametros.read())
    orq_mass_flow = inicializar_orquestrador_mass_flow_teste()
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
    orq_mass_flow = inicializar_orquestrador_mass_flow_teste()
    dados = jsonify(orq_mass_flow.status_equipamentos())
    del(orq_mass_flow)
    return dados



@app.route('/api/check')
def mass_flow_check():
    if not em_execucao:
        return jsonify("Não há o que checar, procedimentos não estão em execução...")
    return jsonify(update_info())



@app.route('/parametros_mass_flow', methods=['GET', 'POST'])
def formulario_parametros_mass_flow():
    if request.method == 'POST':
        with open(parametros_mass_flow, 'w') as params_file:
            dados = request.form['acumulador_de_parametros'].strip('[[').strip(']]').strip('"').replace('","',',').split("],[")
            dados_convertidos = [fluxo_tempo.replace('"',"").split(',') for fluxo_tempo in dados]
            dados_convertidos = [(float(fluxo), int(tempo)) for fluxo, tempo in dados_convertidos]
            json.dump(dados_convertidos, params_file, indent=4)

        return redirect('/')
    
    with open(parametros_mass_flow, 'r') as params_file:
        params = json.loads(params_file.read())

    return render_template('formulario_rotina.html', params=params)


@app.route('/parametros_arduino', methods=['GET', 'POST'])
def formulario_parametros_arduino():
    if request.method == 'POST':
        conf = [{
            "nome": request.form.get('arduino_1'),
            "modelo": request.form.get('arduino_1_model'),
            "porta": request.form.get('arduino_1_porta'),
            "taxa_de_transmissao": int(request.form.get('arduino_1_tax_transmiss')),
            "tempo_espera": int(request.form.get('arduino_1_tempo_espera'))
        }]
        
        with open(arduino_config, 'w') as arduinos_file:
            json.dump(conf, arduinos_file, indent=4)
        
        return redirect('/')
    
    with open(arduino_config) as arduinos_file:
        arduinos = json.loads(arduinos_file.read())

    return render_template('formulario_arduino.html', arduinos=arduinos)


@app.route('/parametros_lcr', methods=['GET', 'POST'])
def formulario_parametros_lcr():
    if request.method == 'POST':

        with open(lcr_config) as lcr_file:
            lcr_conf = json.loads(lcr_file.read())[0]

        lcr_conf['nome'] = request.form.get('lcr_1')
        lcr_conf['porta'] = request.form.get('lcr_1_porta')
        lcr_conf['taxa_de_transmissao'] = request.form.get('lcr_1_tax_transmiss')
        lcr_conf['numero_medidas'] = request.form.get('lcr_1_numero_medidas')

        with open(lcr_config, 'w') as lcr_file:
            json.dump([lcr_conf], lcr_file, indent=4)

        return redirect('/')
    
    with open(lcr_config) as lcr_file:
        lcr_conf = json.loads(lcr_file.read())

    return render_template('formulario_lcr.html', lcrs=lcr_conf)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





