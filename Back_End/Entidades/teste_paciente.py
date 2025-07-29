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
#pac.solicitarAjuda()

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

print("Sistema do Paciente ativo. Pressione Ctrl+C para encerrar.")

try:
    while True:
        print("\n--- MENU ---")
        print("1 - Solicitar ajuda")
        print("2 - Atualizar dados pessoais")
        print("0 - Sair")
        comando = input("> ").strip()

        if comando == "1":
            pac.solicitarAjuda()

        elif comando == "2":
            print("\nDigite os dados atualizados:")
            telefone = input("Novo telefone: ").strip()
            endereco = input("Novo endereço: ").strip()

            novosDados = {
                "login": pac.login,
                "senha": pac.senha,
                "nome": pac.nome,
                "cpf": pac.cpf,
                "dataNascimento": pac.dataNascimento,
                "telefone": telefone or pac.telefone,
                "endereco": endereco or pac.endereco,
                "cuidador": pac.cuidador,
            }

            pac.atualizarDados(novosDados)

        elif comando == "0":
            print("Encerrando...")
            break

        else:
            print("Comando inválido. Tente novamente.")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nInterrompido pelo usuário.")

pac.desconectar()