from ..Entidades.Paciente import Paciente

class PacienteEndpoint:

    def conectar(infos):
        paciente = Paciente(infos["login"],infos["senha"],infos["nome"],
                            infos["cpf"],infos["dataNascimento"],infos["telefone"],
                            infos["endereco"],infos["cuidador"],infos["profSaude"])

        return paciente.conectar()

    def soicitarAjuda(infos):
        paciente = Paciente(infos["login"],infos["senha"],infos["nome"],
                            infos["cpf"],infos["dataNascimento"],infos["telefone"],
                            infos["endereco"],infos["cuidador"],infos["profSaude"])
        
        return paciente.solicitarAjuda()
    
    def atualizarDados(infos):
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
