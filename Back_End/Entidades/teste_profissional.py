import time
from .ProfissionalDeSaude import ProfissionalDeSaude

prof = ProfissionalDeSaude(
    login="medicao",
    senha="medicao",
    nome="Senhor médico",
    cpf="12345678912",
    dataNascimento="01/01/1984",
    telefone="719848276355",
    endereco="Rua J, jorgelandia, número 70",
    crm="CRM123456"
)


prof.conectar()

time.sleep(2)


    
# ✅ MANTÉM O SCRIPT RODANDO
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Encerrando...")
    prof.desconectar()