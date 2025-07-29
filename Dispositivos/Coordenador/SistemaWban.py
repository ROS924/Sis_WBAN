import json
import paho.mqtt.client as mqtt
import os

class SistemaWban:
    def __init__(self):
        self.broker = "broker.hivemq.com"
        self.port = 1883
        self.client = mqtt.Client()
        self.topicoEspSub = "esp32/sub"
        self.topicoEspPub = "esp32/pub"

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

    def carregar_dados(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_json = os.path.join(base_dir, '..', '..', 'BD', 'BD_Entidades.json')
        caminho_json = os.path.normpath(caminho_json)  # Normaliza o caminho para o OS

        with open(caminho_json, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Salva os dados no JSON
    def salvar_dados(self,dados):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_json = os.path.join(base_dir, '..', '..', 'BD', 'BD_Entidades.json')
        caminho_json = os.path.normpath(caminho_json)  # Normaliza o caminho para o OS
        with open(caminho_json, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

    def buscarEntidade(self,db, cpf:str,tipoEntidade:str):
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
        
        topico = f"{entidade_encontrada['tipo']}/{entidade_encontrada['login']}/sub"

        print("Dados registrados com sucesso !")

        return self.publicar(mensagem,topico)
    
    def gerarAlerta(self, cabecalho:dict, dados):
        db = self.carregar_dados()
        destinatario = self.buscarEntidade(db,cpf=cabecalho["usuario_destino"], tipoEntidade=cabecalho['tipo_usuario_destino'])

        if cabecalho["acao"] == "ajuda": #Quando um paciente solicita ajuda
            # Gera o alerta para o profissional de saúde
            menssagem = {
                "acao": "alerta",
                "tipo_usuario_origem": cabecalho["tipo_usuario_origem"],
                "tipo_usuario_destino": cabecalho["tipo_usuario_destino"],
                "usuario_origem":cabecalho["usuario_origem"],
                "usuario_destino": cabecalho["usuario_destino"],
                "dados": dados,
                "msg_texto": f"PACIENTE PRECISA DE AJUDA!!!"
            }

            topico = f"{cabecalho['tipo_usuario_destino']}/{destinatario['login']}/sub"
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

            pac = self.buscarEntidade(db,cabecalho["usuario_origem"],cabecalho["tipo_usuario_origem"])
            topico = f"{cabecalho['tipo_usuario_origem']}/{pac['login']}/sub"
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
            topico = f"{cabecalho['tipo_usuario_destino']},{pac['login']}/sub"
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
        topico = f"{cabecalho['tipo_usuario_origem']}/{pac['login']}/sub"
        self.publicar(menssagem,topico)

    def receberDadosDosSensores(self):
        topico = self.topicoEspSub
        mensagem = "dados"
        self.publicar(mensagem,topico)

    def receberDadosHistorico(self):
        # Precisa ser implementada;
        # talvez um for que use receberDadosDosSensores,
        # ou carregar_dados
        pass


    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker!")
            bd = self.carregar_dados()

            self.client.subscribe(self.topicoEspPub)
            print(f"Inscrito em: {self.topicoEspPub}")

            pacientes = bd["$Paciente"]
            cuidadores = bd["$Cuidador"]
            medicos = bd["$ProfissionalDeSaude"]

            for paciente in pacientes:
                topico = f"{paciente['tipo']}/{paciente['login']}/pub"
                self.client.subscribe(topico)
                print(f"Inscrito em: {topico}")

            for cuidadores in cuidadores:
                topico = f"{cuidadores['tipo']}/{cuidadores['login']}/pub"
                self.client.subscribe(topico)
                print(f"Inscrito em: {topico}")

            for medico in medicos:
                topico = f"{medico['tipo']}/{medico['login']}/pub"
                self.client.subscribe(topico)
                print(f"Inscrito em: {topico}")
            
        else:
            print(f"Erro de conexão: {rc}")

    def on_message(self, client, userdata, msg):       
        mensagem = msg.payload.decode()
        mensagem = json.loads(mensagem)

        if mensagem["acao"] == "ajuda":
            self.receberDadosDosSensores()

        elif mensagem["acao"] == "regis":
            self.armazenarDados(mensagem["dados"],mensagem["usuario_origem"],mensagem["tipo_usuario_origem"])

        elif mensagem["acao"] == "res_ajuda":
            self.gerarAlerta(mensagem,"")
        elif mensagem["acao"] == "ret_dados_ajuda":
            dados = mensagem
            dados.pop("acao",None)
            mes = {
                "acao": "ajuda",
                "tipo_usuario_origem": "Paciente",
                "tipo_usuario_destino": "ProfissionalDeSaude",
                "usuario_origem": dados["cpf"],
                "usuario_destino": dados["medico"],
                "dados": "",
                "msg_texto": ""
            }
            self.gerarAlerta(mes, dados)
        elif mensagem["acao"] == "enviar_recomendacoes":
            db = self.carregar_dados()
            
            # Buscar o paciente (destinatário da recomendação)
            destinatario = self.buscarEntidade(
                db, 
                cpf=mensagem["usuario_destino"], 
                tipoEntidade=mensagem["tipo_usuario_destino"]
            )

            if isinstance(destinatario, str) and "erro" in destinatario:
                print("Erro: destinatário não encontrado")
                return

            topico = f"{mensagem['tipo_usuario_destino']}/{destinatario['login']}/sub"

            nova_msg = {
                "acao": "recomendacao_recebida",
                "tipo_usuario_origem": mensagem["tipo_usuario_origem"],
                "tipo_usuario_destino": mensagem["tipo_usuario_destino"],
                "usuario_origem": mensagem["usuario_origem"],  # CRM do médico
                "usuario_destino": mensagem["usuario_destino"],  # CPF do paciente
                "dados": mensagem["dados"],
                "msg_texto": mensagem["msg_texto"]
            }

            self.publicar(nova_msg, topico)

        elif mensagem["acao"] == "requisitar_exames":
            db = self.carregar_dados()
            
            # Buscar o paciente (destinatário da recomendação)
            destinatario = self.buscarEntidade(
                db, 
                cpf=mensagem["usuario_destino"], 
                tipoEntidade=mensagem["tipo_usuario_destino"]
            )

            if isinstance(destinatario, str) and "erro" in destinatario:
                print("Erro: destinatário não encontrado")
                return

            topico = f"{mensagem['tipo_usuario_destino']}/{destinatario['login']}/sub"

            nova_msg = {
                "acao": "exame_solicitado",
                "tipo_usuario_origem": mensagem["tipo_usuario_origem"],
                "tipo_usuario_destino": mensagem["tipo_usuario_destino"],
                "usuario_origem": mensagem["usuario_origem"],  # CRM do médico
                "usuario_destino": mensagem["usuario_destino"],  # CPF do paciente
                "dados": mensagem["dados"],
                "msg_texto": mensagem["msg_texto"]
            }
            self.publicar(nova_msg, topico)

        return mensagem

    def on_publish(self, client, userdata, mid):
        print(f" Mensagem publicada (ID: {mid})")

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
