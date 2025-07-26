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

   def on_message(client,userdata,msg):
        mensagem = super().on_message(client,userdata,msg)

        if mensagem["acao"] == "res_ajuda":
            notificacao = f"ATUALIZAÇÃO DO PEDIDO DE AJUDA: {mensagem['msg_texto']}"

            return notificacao
        
        elif mensagem["acao"] == "alerta":
            leituras = mensagem["dados"]
            notificacao = f"SUAS LEITURAS BIOMÉTRICAS ESTÃO ANORMAIS !!!\n\n{leituras}"

        elif mensagem["acao"] == "put_ok":
            notificacao = f"{mensagem['msg_texto']} com sucesso !"

        return notificacao
   
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

   '''
   Vai para o raspberry

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
        pacientes = db['Pacientes']
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
        self.salvar_dados(db)'''



      