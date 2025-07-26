import json
from .Usuario import Usuario
from ..Enums import Usuarios 
tipoUsuario = Usuarios.TipoDeUsuario


class Paciente(Usuario): 
   def __init__(self,login:str,senha:str,nome:str, cpf:str, dataNascimento:str, telefone:str,endereco:str,cuidador:str, profSaude:str, tipo = tipoUsuario.Paciente.name):
      super().__init__(login,senha,tipo,nome,cpf,dataNascimento,telefone,endereco)
      self.cuidador = cuidador #CPF do cuidador do paciente
      self.profSaude = profSaude #CRM do profissional de saúde que acompanha o paciente

      self.client.on_message = self.on_message


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

   def on_message(self, client, userdata, msg):
        mensagem = super().on_message(client, userdata, msg)

        if not mensagem:
            return

        notificacao = None  # Inicializa a variável

        if mensagem["acao"] == "res_ajuda":
            notificacao = f"ATUALIZAÇÃO DO PEDIDO DE AJUDA: {mensagem['msg_texto']}"

        elif mensagem["acao"] == "alerta":
            leituras = mensagem["dados"]
            notificacao = f"SUAS LEITURAS BIOMÉTRICAS ESTÃO ANORMAIS !!!\n\n{leituras}"

        elif mensagem["acao"] == "put_ok":
            notificacao = f"{mensagem['msg_texto']} com sucesso !"

        if notificacao:
            print(f"[{self.login}] 📢 Notificação recebida:\n{notificacao}")
            return notificacao
        else:
            print(f"[{self.login}] ⚠️ Mensagem desconhecida: {mensagem}")
            return None
   
   def atualizarDados(self, novosDados:json):
       mensagem = {"acao": "put",
                    "tipo_usuario_origem": self.tipo,
                    "tipo_usuario_destino": None,
                    "usuario_origem": self.cpf,
                    "usuario_destino": None,
                    "dados": novosDados,
                    "msg_texto": ""
                    }
        
       self.publicar(mensagem)


   



      