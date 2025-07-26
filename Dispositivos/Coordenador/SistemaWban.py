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

    def armazenarDados(self, dados:json,cpf:str,solicitante:str):
        db = self.carregar_dados()
        
        # Procura a entidade pelo ID
        entidades = db[f'${solicitante}']
        entidade_encontrada = None
        
        for entidade in entidades:
            if entidade['cpf'] == cpf:
                entidade_encontrada = entidade
                break
        
        if not entidade_encontrada:
            return "erro: entidade não encontrado"
        
        # Atualiza os campos da entidade
        for chave, valor in dados.items():
            if chave in entidade_encontrada:
                entidade_encontrada[chave] = valor
        
        # Salva as alterações no arquivo JSON
        self.salvar_dados(db)

        #Enviar resposta 

        mensagem = {"acao": "res_regis",
                    "tipo_usuario_origem": "",
                    "tipo_usuario_destino": entidade_encontrada["tipo"],
                    "usuario_origem":"",
                    "usuario_destino": entidade_encontrada["cpf"],
                    "dados": "",
                    "msg_texto": "Dados registrados com sucesso !"}
        
        topico = f"{entidade_encontrada["tipo"]}/{entidade_encontrada["login"]}/sub"

        return self.publicar(mensagem,topico)


    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker!")
            bd = self.carregar_dados()

            pacientes = bd["$Pacientes"]
            cuidadores = bd["$Cuidadores"]
            medicos = bd["$ProfissionaisDeSaude"]

            for paciente in pacientes:
                topico = f"{paciente["tipo"]}/{paciente["login"]}/pub"
                self.client.subscribe(topico)
                print(f"Inscrito em: {topico}")

            for cuidadores in cuidadores:
                topico = f"{cuidadores["tipo"]}/{cuidadores["login"]}/pub"
                self.client.subscribe(topico)
                print(f"Inscrito em: {topico}")

            for medico in medicos:
                topico = f"{medico["tipo"]}/{medico["login"]}/pub"
                self.client.subscribe(topico)
                print(f"Inscrito em: {topico}")
            
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

    def publicar(self, mensagem, topico):
        if isinstance(mensagem, dict):
            mensagem = json.dumps(mensagem)
        self.client.publish(topico, mensagem)
        print("topico: ",topico)