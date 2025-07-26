import json
from ..Enums import Usuarios 
import paho.mqtt.client as mqtt

tipoUsuario = Usuarios.TipoDeUsuario

class Usuario:
    def __init__(self,login:str,senha:str,tipo:tipoUsuario,nome:str, cpf:str, dataNascimento:str, telefone:str,endereco:str,broker="broker.hivemq.com", port=1883):
      self.login = login
      self.senha = senha
      self.tipo = tipo
      self.nome = nome
      self.cpf = cpf
      self.dataNascimento = dataNascimento
      self.telefone = telefone
      self.endereco = endereco
      self.broker = broker
      self.port = port
      self.client = mqtt.Client()

      self.topicoSubscribe = f"{self.tipo}/{self.login}/sub"
      self.topicoPublish = f"{self.tipo}/{self.login}/pub"


      self.client.on_connect = self.on_connect
      self.client.on_message = self.on_message
      self.client.on_publish = self.on_publish


    '''def definir_topicos(self):
        """
        Define os tópicos que o usuário assina e publica com base no tipo.
        """
        if self.tipo in tipoUsuario.Paciente.value:
            return {
                "subscribe": f"paciente/{self.login}/sub",
                "publish": f"paciente/{self.login}/pub"
            }
        elif self.tipo in tipoUsuario.ProfissionalDeSaude.value:
            return {
                "subscribe": f"profissional/{self.login}/sub",
                "publish": f"profissional/{self.login}/pub"
            }
        elif self.tipo in tipoUsuario.Cuidador.value:
            return {
                "subscribe": f"cuidador/{self.login}/sub",
                "publish": f"cuidador/{self.login}/pub"
            }
        elif self.tipo in tipoUsuario.Administrador.value:
            return {
                "subscribe": f"sistema/pub",
                "publish": f"sistema/sub"
            }
        return {"subscribe": [], "publish": []}'''

    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print(f"[{self.login}] Conectado ao broker!")
            # Inscrever nos tópicos específicos
            topico = self.topicoSubscribe
            self.client.subscribe(topico)
            print(f"[{self.login}] Inscrito em: {topico}")
        else:
            print(f"Erro de conexão: {rc}")

    def on_message(self, client, userdata, msg):       
        mensagem = msg.payload.decode()
        mensagem = json(mensagem)

        print(f"[{self.login}] Mensagem recebida em {msg.topic}: {mensagem}")

        return mensagem

    def on_publish(self, client, userdata, mid):
        print(f"[{self.login}] Mensagem publicada (ID: {mid})")

    def conectar(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def desconectar(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publicar(self, mensagem):
        topico = self.topicoPublish
        self.client.publish(topico, mensagem)

