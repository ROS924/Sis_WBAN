import time
from ..Enums import Usuarios 
from .ProfissionalDeSaude import ProfissionalDeSaude
from .Paciente import Paciente

# Simula os enums definidos em Enums.Usuarios.TipoDeUsuario
tipoUsuario = Usuarios.TipoDeUsuario

# Criar um profissional de saúde
prof = ProfissionalDeSaude(
    login="drjoao",
    senha="senha123",
    tipo=tipoUsuario.ProfissionalDeSaude.name,
    nome="Dr. João",
    cpf="00011122233",
    dataNascimento="1970-01-01",
    telefone="(71)99999-8888",
    endereco="Rua da Saúde, 100",
    crm="CRM123456"
)

# Criar um paciente
pac = Paciente(
    login="maria123",
    senha="senha456",
    nome="Maria da Silva",
    cpf="99988877766",
    dataNascimento="1985-05-05",
    telefone="(71)98888-7777",
    endereco="Av. das Árvores, 200",
    cuidador="00011122233",      # CPF do cuidador
    profSaude="CRM123456"        # CRM do profissional que acompanha
)

# Conectar ambos
print("Conectando usuário profissional...")
prof.conectar()

print("Conectando usuário paciente...")
pac.conectar()

# Aguardar conexão
time.sleep(2)

# Publicar mensagens simuladas
print("\n[TESTE] Profissional solicitando monitoramento do paciente...")
prof.monitorarPaciente(paciente_id=pac.cpf)

time.sleep(3)

print("\n[TESTE] Profissional acessando histórico do paciente...")
prof.acessarHistorico(paciente_id=pac.cpf)

time.sleep(3)

print("\n[TESTE] Paciente solicitando ajuda...")
pac.solicitarAjuda()

# Aguarde um tempo para garantir que tudo foi enviado
time.sleep(3)

# Desconectar
prof.desconectar()
pac.desconectar()
print("Conexões encerradas.")
