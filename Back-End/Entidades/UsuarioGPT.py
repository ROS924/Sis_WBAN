import paho.mqtt.client as mqtt
#pip install paho-mqtt==2.1.O
class UsuarioMQTT:
    def __init__(self, username, tipo, broker="broker.hivemq.com", port=1883):
        self.username = username
        self.tipo = tipo  # paciente, medico, cuidador, admin
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.topicos = self.definir_topicos()
        
        # Callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

    def definir_topicos(self):
        """
        Define os tópicos que o usuário assina e publica com base no tipo.
        """
        if self.tipo == "paciente":
            return {
                "subscribe": [f"paciente/{self.username}/comando"],
                "publish": [f"paciente/{self.username}/dados", f"paciente/{self.username}/ajuda"]
            }
        elif self.tipo == "medico":
            return {
                "subscribe": [f"medico/{self.username}/alertas"],
                "publish": [f"medico/{self.username}/comando"]
            }
        elif self.tipo == "cuidador":
            return {
                "subscribe": [f"cuidador/{self.username}/notificacoes"],
                "publish": []
            }
        elif self.tipo == "admin":
            return {
                "subscribe": [f"sistema/logs"],
                "publish": [f"sistema/comandos"]
            }
        return {"subscribe": [], "publish": []}

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[{self.username}] Conectado ao broker!")
            # Inscrever nos tópicos específicos
            for topico in self.topicos['subscribe']:
                client.subscribe(topico)
                print(f"[{self.username}] Inscrito em: {topico}")
        else:
            print(f"Erro de conexão: {rc}")

    def on_message(self, client, userdata, msg):
        print(f"[{self.username}] Mensagem recebida em {msg.topic}: {msg.payload.decode()}")

    def on_publish(self, client, userdata, mid):
        print(f"[{self.username}] Mensagem publicada (ID: {mid})")

    def conectar(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def desconectar(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publicar(self, topico, mensagem):
        if topico in self.topicos['publish']:
            self.client.publish(topico, mensagem)
        else:
            print(f"[{self.username}] Não tem permissão para publicar em {topico}")
