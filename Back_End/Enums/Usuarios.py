from enum import Enum

class TipoDeUsuario(Enum):
    Paciente = ["Paciente","paciente"]
    ProfissionalDeSaude = ["Profissional de Saúde", "profissional de saude", "profissional de saúde","ProfissionalDeSaude"]
    Cuidador = ["Cuidador","cuidador"]
    Administrador = ["Administrador","administrador", "adm","Adm","admin","Admin"]