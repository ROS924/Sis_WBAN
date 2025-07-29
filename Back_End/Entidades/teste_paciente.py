import time
from .Paciente import Paciente
from .Usuario import Usuario


pac = Paciente(
    login="jjObrabo",
    senha="jjObrabo",
    nome="jorge júnior",
    cpf="12345678910",
    dataNascimento="01/01/2010",
    telefone="719848276333",
    endereco="Rua J, jorgelandia, número 10",
    cuidador="12345678911",      # CPF do cuidador
    profSaude="CRM123456"        # CRM do profissional que acompanha
)



pac.conectar()

# Aguardar conexão
time.sleep(4)
pac.solicitarAjuda()

novosDados = {
    "login":"jjObrabo",
    "senha":"jjObrabo",
    "nome":"jorge júnior",
    "cpf":"12345678910",
    "dataNascimento":"01/01/2010",
    "telefone":"71912344321",
    "endereco":"Rua J, jorgelandia, número 10",
    "cuidador":"12345678911",      
    }

#pac.atualizarDados(novosDados)

# ✅ MANTÉM O SCRIPT RODANDO
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Encerrando...")
    pac.desconectar()