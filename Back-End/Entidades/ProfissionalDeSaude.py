from .Usuario import Usuario
from ..Enums import Usuarios 
tipoUsuario = Usuarios.TipoDeUsuario

class ProfissionalDeSaude(Usuario): 
   def __init__(self,login:str,senha:str,tipo:tipoUsuario,nome:str, cpf:str, dataNascimento:str, telefone:str,endereco:str,crm:str):
      super().__init__(login,senha,tipo,nome,cpf,dataNascimento,telefone,endereco)
      self.crm = crm

   def monitorarPaciente(self, paciente_id: str):
      """
      Solicita ao sistema os dados mais recentes de um paciente.
      """
      mensagem = {
         "acao": "monitorar",
         "tipo_usuario_origem": self.tipo,
         "tipo_usuario_destino": "SistemsWBAN",
         "usuario_origem": self.crm,
         "usuario_destino": "",
         "dados": paciente_id,
         "msg_texto": ""
      }
      self.publicar(mensagem)

   def acessarHistorico(self, paciente_id: str):
      """
      Solicita o histórico clínico de um paciente.
      """
      mensagem = {
         "acao": "historico",
         "tipo_usuario_origem": self.tipo,
         "tipo_usuario_destino": tipoUsuario.ProfissionalDeSaude.name,
         "usuario_origem": self.crm,
         "usuario_destino": "",
         "dados": paciente_id,
         "msg_texto": ""
      }
      self.publicar(mensagem)


   def receberAlertas(self, mensagem: dict):
        """
        Callback para processar alertas recebidos via MQTT.
        """
        print(f"[Alerta] {mensagem}")

   def analisarTendencias(self, paciente_id: str):
      """
      Solicita ao sistema a análise gráfica de tendências de saúde.
      """
      mensagem = {
      "acao": "analisar_tendencias",
      "tipo_usuario_origem": self.tipo,
      "tipo_usuario_destino": "SistemsWBAN",
      "usuario_origem": self.crm,
      "usuario_destino": "",
      "dados": paciente_id,
      "msg_texto": ""
      }
      self.publicar(mensagem)

   def registrarDiagnostico(self, paciente_id: str, diagnostico: str):
        """
        Registra um diagnóstico no sistema.
        """

   def diagnosticarCondicoes(self, paciente_id: str, dados: dict):
        """
        Processa dados clínicos para auxiliar no diagnóstico.
        """
        mensagem = {
        "acao": "enviar_recomendacoes",
        "tipo_usuario_origem": self.tipo,
        "tipo_usuario_destino": tipoUsuario.Paciente,
        "usuario_origem": self.crm,
        "usuario_destino": paciente_id,
        "dados": "",
        "msg_texto": dados
        }
        self.publicar(mensagem)

   def emitirRequisicaoExames(self, paciente_id: str):
        """
        Emite requisição de exames para um paciente.
        """
        mensagem = {
        "acao": "requisitar_exames",
        "tipo_usuario_origem": self.tipo,
        "tipo_usuario_destino": tipoUsuario.Paciente,
        "usuario_origem": self.crm,
        "usuario_destino": paciente_id,
        "dados": "",
        "msg_texto": ""
        }
        self.publicar(mensagem)

   def enviarRecomendacoes(self, paciente_id: str, recomendacoes: str):
        """
        Envia recomendações clínicas para um paciente/cuidador.
        """
        mensagem = {
        "acao": "enviar_recomendacoes",
        "tipo_usuario_origem": self.tipo,
        "tipo_usuario_destino": tipoUsuario.Paciente,
        "usuario_origem": self.crm,
        "usuario_destino": paciente_id,
        "dados": "",
        "msg_texto": recomendacoes
        }
        self.publicar(mensagem)

      