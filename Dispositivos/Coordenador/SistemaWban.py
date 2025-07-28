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

    def buscarEntidade(db, cpf:str,tipoEntidade:str):
        # Procura a entidade pelo ID
        entidades = db[f'${tipoEntidade}']
        entidade_encontrada = None

        if tipoEntidade == "ProfissionalDeSaude":
            for entidade in entidades:
                if entidade['crm'] == cpf:
                    entidade_encontrada = entidade
                    return entidade_encontrada
        else:
            for entidade in entidades:
                if entidade['cpf'] == cpf:
                    entidade_encontrada = entidade
                    return entidade_encontrada
        
        if not entidade_encontrada:
            return "erro: entidade não encontrado"

    def armazenarDados(self, dados:json,cpf:str,solicitante:str):
        db = self.carregar_dados()
        
        entidade_encontrada = self.buscarEntidade(db,cpf,solicitante)
        
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

        print("Dados registrados com sucesso !")

        return self.publicar(mensagem,topico)
    
    def gerarAlerta(self, cabecalho:dict, dados):
        destinatario = self.buscarEntidade(cabecalho["usuario_destino"], cabecalho["tipo_usuario_destino"])

        if cabecalho["acao"] == "ajuda": #Quando um paciente solicita ajuda
            # Gera o alerta para o profissional de saúde
            menssagem = {
                "acao": "alerta",
                "tipo_usuario_origem": cabecalho["tipo_usuario_origem"],
                "tipo_usuario_destino": cabecalho["tipo_usuario_destino"],
                "usuario_origem":cabecalho["usuario_origem"],
                "usuario_destino": cabecalho["usuario_destino"],
                "dados": dados,
                "msg_texto": ""
            }

            topico = f"{cabecalho["tipo_usuario_destino"]}/{destinatario["login"]}/sub"
            self.publicar(menssagem,topico)

            # Gera a resposta para o paciente
            menssagem = {
                "acao": "res_ajuda",
                "tipo_usuario_origem": "",
                "tipo_usuario_destino": cabecalho["tipo_usuario_origem"],
                "usuario_origem":"",
                "usuario_destino": cabecalho["usuario_origem"],
                "dados": "",
                "msg_texto": "Pedido de ajuda enviado"
            }

            pac = self.buscarEntidade(cabecalho["usuario_origem"],cabecalho["tipo_usuario_origem"])
            topico = f"{cabecalho["tipo_usuario_origem"]},{pac["login"]}/sub"
            self.publicar(menssagem, topico)

        elif cabecalho["acao"] == "res_alerta": #Quando o médico responde o pedido de ajuda
            # origem -> médico
            # destino -> paciente
            #Envia a resposta ao paciente
            menssagem = {
                "acao": "res_ajuda",
                "tipo_usuario_origem": cabecalho["tipo_usuario_origem"],
                "tipo_usuario_destino": cabecalho["tipo_usuario_destino"],
                "usuario_origem":cabecalho["usuario_origem"],
                "usuario_destino": cabecalho["usuario_destino"],
                "dados": "",
                "msg_texto": "Ajuda a cominho !!"
            }

            pac = self.buscarEntidade(cabecalho["usuario_destino"],cabecalho["tipo_usuario_destino"])
            topico = f"{cabecalho["tipo_usuario_destino"]},{pac["login"]}/sub"
            self.publicar(menssagem, topico)

    def retornarDadosHistorico(self, cabecalho:dict):
        # Retorna os dados do paciente pro profissional
        dados = self.receberDadosHistorico()
        menssagem = {
            "acao": "res_historico",
            "tipo_usuario_origem": "",
            "tipo_usuario_destino": cabecalho["tipo_usuario_origem"],
            "usuario_origem":"",
            "usuario_destino": cabecalho["usuario_origem"],
            "dados": dados,
            "msg_texto": "Dados retornados"
        }
        pac = self.buscarEntidade(cabecalho["usuario_origem"],cabecalho["tipo_usuario_origem"])
        topico = f"{cabecalho["tipo_usuario_origem"]}/{pac["login"]}/sub"
        self.publicar(menssagem,topico)

    def receberDadosDosSensores():
        #Precisa ser implementada
        pass
    def receberDadosHistorico():
        # Precisa ser implementada;
        # talvez um for que use receberDadosDosSensores,
        # ou carregar_dados
        pass


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
        mensagem = json.loads(mensagem)

        if mensagem["acao"] == "ajuda":
            dados = self.receberDadosDosSensores()
            self.gerarAlerta(mensagem,dados)

        elif mensagem["acao"] == "regis":
            self.armazenarDados(mensagem["dados"],mensagem["usuario_origem"],mensagem["tipo_usuario_origem"])

        elif mensagem["acao"] == "res_ajuda":
            self.gerarAlerta(mensagem,"")

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