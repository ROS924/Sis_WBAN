from flask import Flask, request
from .Endpoints.Paciente_endpoints import PacienteEndpoint

app = Flask(__name__)

paciente = PacienteEndpoint()

#Endpoints do Paciente

@app.route("/paciente/conectar", methods=["POST"])
def conectar():
    infos = request.get_json()
    return paciente.conectar(infos)

@app.route("/paciente/solicitarajuda", methods=["POST"])
def soicitarAjuda():
    infos = request.get_json()
    return paciente.soicitarAjuda(infos)

@app.route("/paciente/atualizardados",methods=["POST"])
def atualizarDados():
    infos = request.get_json()
    return paciente.atualizarDados(infos)

if __name__ == '__main__':
    app.run(debug=True)