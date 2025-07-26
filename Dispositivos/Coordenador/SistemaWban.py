import json
import paho.mqtt.client as mqtt


class SistemaWban:
    def __init__(self):
        self.broker = "broker.hivemq.com"
        self.port = 1883
        self.client = mqtt.Client()



    def carregar_dados():
        with open('.../BD/BD_Entidades.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    # Salva os dados no JSON
    def salvar_dados(dados):
        with open('.../BD/BD_Entidades.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

    def atualizarDadosPessoais(self, novosDados:json,cpf:str):
        db = self.carregar_dados()
        
        # Procura o paciente pelo ID
        pacientes = db['$Pacientes']
        paciente_encontrado = None
        
        for paciente in pacientes:
            if paciente['cpf'] == cpf:
                paciente_encontrado = paciente
                break
        
        if not paciente_encontrado:
            return "erro: Paciente não encontrado"
        
        # Atualiza os campos do paciente
        for chave, valor in novosDados.items():
            if chave in paciente_encontrado:
                paciente_encontrado[chave] = valor
        
        # Salva as alterações no arquivo JSON
        self.salvar_dados(db)






    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:

            bd = self.carregar_dados()

            pacientes = bd["$Pacientes"]
            cuidadores = bd["$Cuidadores"]
            medicos = bd["$ProfissionaisDeSaude"]

            for paciente in pacientes:
                topico = f"{paciente["tipo"]}/{paciente["login"]}/pub"

            for cuidadores in cuidadores:
                topico = f"{cuidadores["tipo"]}/{cuidadores["login"]}/pub"

            for medico in medicos:
                topico = f"{medico["tipo"]}/{medico["login"]}/pub"

            print(f"[{self.login}] Conectado ao broker!")
            # Inscrever nos tópicos específicos
            topico = self.topicoSubscribe
            self.client.subscribe(topico)
            print(f"[{self.login}] Inscrito em: {topico}")
        else:
            print(f"Erro de conexão: {rc}")

    def on_message(self, client, userdata, msg):       
        mensagem = msg.payload.decode()
        #mensagem = json(mensagem)
        mensagem = json.loads(mensagem)

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
        if isinstance(mensagem, dict):
            mensagem = json.dumps(mensagem)
        self.client.publish(topico, mensagem)
        print("topico: ",topico)