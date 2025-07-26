from flask import Flask, request
from ..Entidades.Paciente import Paciente

class PacienteEndpoint:

    app = Flask(__name__)


    @app.route("/paciente/conectar", methods=["GET"])
    def conectar():
        infos = request.get_json()

        paciente = Paciente(infos["login"],infos["senha"],infos["nome"],
                            infos["cpf"],infos["dataNascimento"],infos["telefone"],
                            infos["endereco"],infos["cuidador"],infos["profSaude"])

        return paciente.conectar()

    @app.route("/paciente/solicitarajuda", methods=["GET"])
    def soicitarAjuda():
        infos = request.get_json()

        paciente = Paciente(infos["login"],infos["senha"],infos["nome"],
                            infos["cpf"],infos["dataNascimento"],infos["telefone"],
                            infos["endereco"],infos["cuidador"],infos["profSaude"])
        
        return paciente.solicitarAjuda()
    
    @app.route("/paciente/atualizardados",methods=["POST"])
    def atualizarDados():
        infos = request.get_json()

        paciente = Paciente(infos["login"],infos["senha"],infos["nome"],
                            infos["cpf"],infos["dataNascimento"],infos["telefone"],
                            infos["endereco"],infos["cuidador"],infos["profSaude"])
        
        novasInfos = {
            "login": infos["login"],
            "senha": infos["senha"],
            "nome": infos["novoNome"],
            "cpf": infos["cpf"],
            "dataNascimento":infos["dataNascimento"],
            "telefone": infos["novoTelefone"],
            "endereco": infos["novoEndereco"],
            "cuidador": infos["novoCuidador"],
            "profSaude": infos["novoProfSaude"],
            "tipo": "Paciente"
        }

        return paciente.atualizarDados(novasInfos)
