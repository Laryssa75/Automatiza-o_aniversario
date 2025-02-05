from .models import Funcionario
from .models import UsuarioBasico

#Calculo do cbo ao inserir
def obter_proximo_cbo():  
    #Obtem todos os números de cbo existentes
    cbos_existentes = list(Funcionario.objects.values_list('cbo', flat=True).order_by('cbo'))

    if not cbos_existentes:
        return 1
    
    if len(cbos_existentes) == 1:
        return cbos_existentes[0] + 1

    #Verifica as colunas no intervalo
    for i in range(1, len(cbos_existentes)):
        if cbos_existentes[i] != cbos_existentes[i - 1] + 1:
            return cbos_existentes[i - 1] + 1

    #Se não houver lacunas, retorna o próximo número após o maior
    return cbos_existentes[-1] + 1 
        

def obter_proximo_idUSu():
    #Obtem todos os números de idUsu existentes
    idUsu_existente = list(UsuarioBasico.objects.values_list('id_usuario', flat=True).order_by('id_usuario'))

    if not idUsu_existente:
        return 1
    
    if len(idUsu_existente) == 1:
        return idUsu_existente[0] + 1

    #Verifica as colunas no intervalo
    for i in range(1, len(idUsu_existente)):
        if idUsu_existente[i] != idUsu_existente[i - 1] + 1:
            return idUsu_existente[i - 1] + 1
        
    return idUsu_existente[-1] +1 
