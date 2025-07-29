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

print("Sistema ativo. Pressione Ctrl+C para encerrar.")

try:
    while True:
        print("\n--- MENU ---")
        print("1 - Enviar recomendação ao paciente")
        print("2 - Emitir requisição de exames")
        print("0 - Sair")
        comando = input("> ").strip()

        if comando == "1":
            recomendacao = input("Digite a recomendação: ")
            prof.enviarRecomendacoes("12345678910", recomendacao)

        elif comando == "2":
            exames = input("Digite os exames a requisitar: ")
            prof.emitirRequisicaoExames("12345678910", exames)

        elif comando == "0":
            print("Encerrando...")
            break

        else:
            print("Comando inválido. Tente novamente.")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nInterrompido pelo usuário.")

prof.desconectar()