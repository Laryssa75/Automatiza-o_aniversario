from .models import Funcionario
from .models import Usuario

#Calculo do cbo ao inserir
def obter_proximo_cbo():  
    #Obtem todos os números de cbo existentes
    cbos_existentes = list(Funcionario.objects.values_list('cbo', flat=True).order_by('cbo'))

    #Verifica as colunas no intervalo
    for i in range(1, len(cbos_existentes)):
        if cbos_existentes[i] != cbos_existentes[i - 1] + 1:
            return cbos_existentes[i - 1] + 1

   #Se não houver lacunas, retorna o próximo número após o maior
    return cbos_existentes[-1] + 1 if cbos_existentes else 1


def reorganizar_cbo():
    #Obtem todos os funcionários ordenados por cbo
    funcionarios = Funcionario.objects.all().order_by('cbo')

    #Atualiza o número de cbo de forma sequencial
    for index, funcionario in enumerate(funcionarios, start=1):
        funcionario.cbo = index
        funcionario.save()

def obter_proximo_idUSu():
    #Obtem todos os números de idUsu existentes
    idUsu_existente = list(Usuario.objects.values_list('id_usuario', flat=True).order_by('id_usuario'))

    #Verifica as colunas no intervalo
    for i in range(1, (idUsu_existente)):
        if idUsu_existente[i] != idUsu_existente[i -1] + 1:
            return idUsu_existente[i - 1] + 1
        
    return idUsu_existente[-1] +1 if idUsu_existente else 1


def reorganizar_idUSu():
    #obtem todos os usuarios ordenados por idUsu
    usuario = Usuario.objects.all().order_by('id_usuario')

    #Atualiza o número de idUsu de forma sequencial
    for index, usuario in enumerate(usuario, start=1):
        usuario.id_usuario = index
        usuario.save()