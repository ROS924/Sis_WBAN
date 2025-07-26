from .Usuario import Usuario
from ..Enums import Usuarios 
tipoUsuario = Usuarios.TipoDeUsuario

class Cuidador(Usuario): 
    def __init__(self, login: str, senha: str, nome: str, cpf: str, 
                 dataNascimento: str, telefone: str, endereco: str, parentesco: str, tipo= tipoUsuario.Cuidador.name):
        super().__init__(login, senha, tipo, nome, cpf, dataNascimento, telefone, endereco)
        self.parentesco = parentesco

    def monitorarPaciente(self, paciente_id: str):
        """
        Acessa informações básicas sobre o estado de saúde do paciente.
        """
        mensagem = {
            "acao": "monitorar",
            "tipo_usuario_origem": self.tipo,
            "tipo_usuario_destino": tipoUsuario.Paciente,
            "usuario_origem": self.cpf,
            "usuario_destino": paciente_id,
            "dados": paciente_id,
            "msg_texto": ""
        }
        self.publicar(mensagem)

    def receberAlertas(self, mensagem: dict):
        """
        Callback para processar alertas recebidos via MQTT.
        """
        print(f"[Alerta Cuidador] {mensagem}")

    def enviarFeedback(self, paciente_id: str, feedback: str):
        """
        Envia feedback ao profissional de saúde sobre o paciente.
        """
        mensagem = {
            "acao": "enviar_feedback",
            "tipo_usuario_origem": self.tipo,
            "tipo_usuario_destino": tipoUsuario.ProfissionalDeSaude.name,
            "usuario_origem": self.login,
            "usuario_destino": "",
            "dados": paciente_id,
            "msg_texto": feedback
        }
        self.publicar(mensagem)
