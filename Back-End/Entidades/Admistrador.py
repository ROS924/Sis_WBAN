from .Usuario import Usuario
from ..Enums import Usuarios 
tipoUsuario = Usuarios.TipoDeUsuario
from Entidades.Paciente import Paciente
from Entidades.ProfissionalDeSaude import ProfissionalDeSaude

class Administrador(Usuario):
    def __init__(self, login: str, senha: str, nome: str, cpf: str, dataNascimento: str, telefone: str, endereco: str, tipo=tipoUsuario.Administrador.name):
        super().__init__(login, senha, tipo, nome, cpf, dataNascimento, telefone, endereco)

    """
        Criar contas de profissionais, cuidadores e pacientes
        Editar contas de profissionais, cuidadores e pacientes
        Excluir contas de profissionais, cuidadores e pacientes
        Listar dispositivos cadastrados                                 - DISPOSITIVOS
        Listar dispositivos conectados                                  - DISPOSITIVOS
        Adicionar dispositivos                                          - DISPOSITIVOS
        Remover dispositivos                                            - DISPOSITIVOS            
        Configurar dispositivos: atualizar sensores e gateways WBAN.    - DISPOSITIVOS
        Reiniciar o sistema                                             - DISPOSITIVOS
        Fazer Backup do Sistema                                         - DISPOSITIVOS     
    """

    def criarConta(self, login: str, senha: str, nome: str, cpf: str, dataNascimento: str, telefone: str, endereco: str, tipo: tipoUsuario):
        try:
            if tipo == tipoUsuario.ProfissionalDeSaude.name:
                crm = input("Digite o CRM do profissional de saúde: ")
                conta = ProfissionalDeSaude(login, senha, nome, cpf, dataNascimento, telefone, endereco, crm)
            elif tipo == tipoUsuario.Cuidador.name:
                # Implementar lógica para criar conta de cuidador
                pass
            elif tipo == tipoUsuario.Paciente.name:
                cuidador = input("Digite o CPF do cuidador: ")
                profSaude = input("Digite o CRM do profissional de saúde: ")
                conta = Paciente(login, senha, nome, cpf, dataNascimento, telefone, endereco, cuidador, profSaude)
        except Exception as e:
            print(f"Erro ao criar conta: {e}\nVerifique o tipo de usuário e os dados fornecidos.")
            return None
        return conta

    def gerenciarConta(self, user: Usuario, codigo: str):
            # Implementar lógica para editar valores de conta, ativando ou desativando usuários
            match codigo:
                case "e":
                    print("Digite o código do dado que deseja editar:\n")
                    print("1 - Nome\n2 - CPF\n3 - Data de Nascimento\n4 - Telefone\n5 - Endereço")
                    isinstance(user, Paciente) and print("6 - CPF do Cuidador\n7 - CRM do Profissional de Saúde")
                    isinstance(user, ProfissionalDeSaude) and print("6 - CRM")
                    print("0 - Cancelar operação")
                    codigo_editar = int(input())
                    match codigo_editar:
                        case 1:
                            user.nome = input("Digite o novo nome: ")
                        case 2:
                            user.cpf = input("Digite o novo CPF: ")
                        case 3:
                            user.dataNascimento = input("Digite a nova data de nascimento (DD/MM/AAAA): ")
                        case 4:
                            user.telefone = input("Digite o novo telefone: ")
                        case 5:
                            user.endereco = input("Digite o novo endereço: ")
                        case 6 if isinstance(user, Paciente):
                            user.cuidador = input("Digite o novo CPF do cuidador: ")
                        case 7 if isinstance(user, Paciente):
                            user.profSaude = input("Digite o novo CRM do profissional de saúde: ")
                        case 6 if isinstance(user, ProfissionalDeSaude):
                            user.crm = input("Digite o novo CRM: ")
                        case 0:
                            print("Operação cancelada.")
                        case _:
                            print("Código inválido. Operação cancelada.")
                case "a":
                    # Ativar conta
                    pass
                case "d":
                    # Desativar conta
                    pass
                case _:
                    print("Código inválido. Use 'e' para editar, 'a' para ativar ou 'd' para desativar.")

    def deletarConta(self, user):
        # Requer acesso a banco de dados
        pass