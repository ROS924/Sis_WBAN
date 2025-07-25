from .Usuario import Usuario
from ..Enums import Usuarios 
tipoUsuario = Usuarios.TipoDeUsuario

class Paciente(Usuario): 
   def __init__(self,login:str,senha:str,nome:str, cpf:str, dataNascimento:str, telefone:str,endereco:str,cuidador:str, profSaude:str, tipo = tipoUsuario.Paciente.name):
      super().__init__(login,senha,tipo,nome,cpf,dataNascimento,telefone,endereco)
      self.cuidador = cuidador #CPF do cuidador do paciente
      self.profSaude = profSaude #CRM do profissional de saúde que acompanha o paciente


   def solicitarAjuda(self):
    mensagem = {"acao": "ajuda",
                "tipo_usuario_origem": self.tipo,
                "tipo_usuario_destino": tipoUsuario.ProfissionalDeSaude.name,
                "usuario_origem": self.cpf,
                "usuario_destino": self.profSaude,
                "dados": "",
                "msg_texto": ""
                }
    
    self.publicar(mensagem)

    

      