import time

from flask import jsonify, Flask
from flask import render_template, request, redirect

from mass_flow_client import send_message

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/run')
def mass_flow_run():
    resposta = send_message('run')
    return jsonify(resposta)

@app.route('/api/stop')
def mass_flow_stop():
    resposta = send_message('stop')
    return jsonify(resposta)

@app.route('/api/check')
def mass_flow_check():
    resposta = send_message('check')
    return jsonify(resposta)


@app.route('/rotina_experimental')
def formulario_exp():
    if request.method == 'POST':
        pass
        return redirect('/')
        
    return render_template('formulario_exp.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





