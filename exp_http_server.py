import json

from flask import jsonify, Flask
from flask import render_template, request, redirect

from mass_flow_setup import inicializar_orquestrador


### Variáveis globais
em_execucao = False
o1 = inicializar_orquestrador()
app = Flask(__name__)


print(f" * Servidor MassFlow iniciando...")



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/api/run')
def mass_flow_run():
    global em_execucao, o1
    em_execucao = True
    lista_fluxo_nao_ar_tempo = None
    with open('parametros.json', 'r') as arquivo_parametros:
        lista_fluxo_nao_ar_tempo = json.loads(arquivo_parametros.read())
    o1 = inicializar_orquestrador()
    o1.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)
    o1.executar_rotina()
    return jsonify("Procedimento iniciado...")



@app.route('/api/stop')
def mass_flow_stop():
    global em_execucao, o1
    em_execucao = False
    o1.interromper()
    return jsonify("Procedimento interrompido...")



@app.route('/api/equipo')
def mass_flow_equipo():
    return jsonify(o1.status_equipamentos())



@app.route('/api/check')
def mass_flow_check():
    if not em_execucao:
        return jsonify("Não há o que checar, procedimentos não estão em execução...")
    return jsonify(o1.status_das_rotinas_em_execucao())



@app.route('/rotina_experimental', methods=['GET', 'POST'])
def formulario_exp():
    if request.method == 'POST':
        pass
        return redirect('/')
    return render_template('formulario_rotina.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





