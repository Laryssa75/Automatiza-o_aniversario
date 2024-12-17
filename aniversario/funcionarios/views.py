import pandas as pd
import logging
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import authenticate, login 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.db import models
from django.contrib import messages
from .models import Funcionario
from .forms import FuncionarioForm, UploadExcelForm
from .tasks import enviar_email_aniversario
from datetime import datetime



#serve para disparar envio de email manualmente
# async def enviar_emails_aniversariantes_view(request):
#     await asyncio.to_thread(enviar_email_aniversario.apply_async)
#     return JsonResponse({"status": "sucess", "message": "E-mails de aniversariantes enviados."})

logger = logging.getLogger(__name__)

def home(request):
    #return HttpResponse("Página inicial do app funcionários")
    return render(request, 'funcionarios/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff: #Verifica se é admin
                return redirect('admin:index') #Redireciona para o painel de admin
            else:
                return redirect('importar_funcionarios')  
        else:        
            #Caso o login falhe
            messages.error(request, "Usuário ou senha inválidos")
            return render(request, 'funcionarios/login.html') 
    
    return render(request, 'funcionarios/login.html') #Renderiza a página de login

#Calculo do cbo
def obter_proximo_cbo():    
   #Obtem o maior valor existente de cbo
    max_cbo = Funcionario.objects.aggregate(models.Max('cbo'))['cbo__max']
    return max_cbo + 1 if max_cbo is not None else 1 


@permission_required('funcionarios.importar_funcionarios', raise_exception=True)
def importar_funcionarios(request, cbo=None):

    #Formularios
    form_funcionario = FuncionarioForm(request.POST or None)
    form_import = UploadExcelForm(request.POST or None, request.FILES or None)

    tarefa_enfileirada = False #Variável para rastrear se a tarefa será enfileirada

    #Criação ou Edição de Funcionários     
    if cbo:
        funcionario = get_object_or_404(Funcionario, cbo=cbo)
        form_funcionario = FuncionarioForm(request.POST or None, instance=funcionario)

    if form_funcionario.is_valid():
        funcionario = form_funcionario.save(commit=False)
        if not cbo: #se não for edição, atribui o próximo CBO
            funcionario.cbo = obter_proximo_cbo() #Atribui o próximo valor de cbo
            form_funcionario.save() #Salva o funcionario

            #Alteração para que o envio do email seja imediato quando se insere os dados dos funcionários via web
            #enviar_email_aniversario.apply_async()

            tarefa_enfileirada = True #Marca que a tarefa será enfileirada

            return redirect('menu_cadastros')


    if request.method == 'POST':
        # Envio de dados manual
        if 'manual' in request.POST:
            if form_funcionario.is_valid():
                funcionario = form_funcionario.save(commit=False)
                if not cbo:
                    funcionario.cbo = obter_proximo_cbo()  # Atribui o próximo valor de cbo
                form_funcionario.save()  # Salva o funcionário
                messages.success(request, "Funcionário adicionado com sucesso!")
                tarefa_enfileirada = True
            else:
                messages.error(request, "Erro ao adicionar funcionário.")


        #Se for envio de dados via arquivo excel
        elif 'import' in request.POST and request.FILES.get('excel_file'):
            form_import = UploadExcelForm(request.POST, request.FILES)
            if form_import.is_valid():
                excel_file = request.FILES['excel_file']
                try:
                    df = pd.read_excel(excel_file)

                    for _, row in df.iterrows():
                        if 'NOME' in row and 'EMAIL' in row and 'DATA NASCIMENTO' in row:
                            Funcionario.objects.create(
                                nome=row['Nome'],
                                email=row['Email'],
                                data_nascimento=row['Data Nascimento'],
                                data_admissao=row.get['Data Admissão', None],
                                funcao=row.get['Função', None],
                                cbo=obter_proximo_cbo() #atribui o próximo valor de id sequencial
                            )

                            tarefa_enfileirada = True #Marca que a tarefa será enfileirada

                        else:
                            messages.error(request, "Arquivo inválido: algumas colunas estão faltando.")
                            break
                    messages.success(request, "Funcionarios importados com sucesso!")
                    print("Funcionarios importados com sucesso!")


                    #return redirect('importar_funcionarios')

                    #Chama a tarefa celery para envio de email de aniversario
                    #enviar_email_aniversario.apply_async()
                
                except Exception as e:
                    messages.error(request, f"Erro ao importar os dados os funcionários: {e}")
                    print("Erro ao importar o arquivo excel!")



    # ** Enfileira a tarefa após as operações de criação **
    if tarefa_enfileirada:
        enviar_email_aniversario.apply_async()

    return render(request, 'funcionarios/importar_funcionario.html', {
        'form_funcionario': form_funcionario,
        'form_import': form_import,
    })


def menu_cadastros(request):
    #Buscar todos os funcionáris cadastrados
    funcionarios = Funcionario.objects.all()
    print(funcionarios)
    logging.info(funcionarios)
    return render(request, 'funcionarios/cadastros.html', {'funcionarios' : funcionarios})


def editar_funcionarios(request, cbo):
    funcionario = get_object_or_404(Funcionario, cbo=cbo)
    print(f"Funcionario encontrado: {funcionario.nome}")
    print(f"cbo encontrado: {funcionario.cbo}")
    print(f"data nascimento encontrado: {funcionario.data_nascimento}")

    if request.method == 'POST':
        form_editar = FuncionarioForm(request.POST, instance=funcionario)
        print(f"dados recebidos:  {request.POST}")
        print(f"Formulário validado: {form_editar.is_valid()}")
        print(f"Erros no formulário: {form_editar.errors}")
        # Criação de formulário com os dados do POST
        print(f"Funcionario encontrado: {funcionario.nome}")
        print(f"Funcionario encontrado: {funcionario.data_nascimento}")

        if form_editar.is_valid():
            print(f"Funcionario encontrado: {funcionario.cbo}")
            form_editar.save()  # Salva o funcionário com os dados corrigidos
            messages.success(request, "Funcionário alterado com sucesso.")
            return redirect('menu_cadastros')
        else:
            messages.error(request, "Falha ao editar o cadastro do funcionário.")
            print(form_editar.errors)  #Para depuração

    else:
        # Quando o método não for POST, preenche o formulário com os dados do funcionário
        form_editar = FuncionarioForm(instance=funcionario)

    return render(request, 'funcionarios/importar_funcionario.html', {
        'form_funcionario': form_editar,
    })


def excluir_funcionario(request, cbo):
    if request.method == "POST":
        funcionario = get_object_or_404(Funcionario, cbo=cbo)
        funcionario.delete()
        messages.success(request, "Funcionário excluído com sucesso.")
    return redirect('menu_cadastros')


def logout_and_redirect(request):
    logout(request)
    #return render (request, 'funcionarios/login.html') #esse caminho faz o caminho para o template login.html
    return redirect('login') #esse caminho faz o redirecionamento da url
