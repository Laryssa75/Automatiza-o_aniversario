import pandas as pd
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from .models import Funcionario
from django.db import models
from django.contrib.auth import logout
from .forms import FuncionarioForm, UploadExcelForm
from django.contrib import messages
from django.http import HttpResponse
from .tasks import enviar_email_aniversario

#serve para disparar envio de email manualmente
# async def enviar_emails_aniversariantes_view(request):
#     await asyncio.to_thread(enviar_email_aniversario.apply_async)
#     return JsonResponse({"status": "sucess", "message": "E-mails de aniversariantes enviados."})

def home(request):
    #return HttpResponse("Página inicial do app funcionários")
    return render(request, 'funcionarios/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff: #Verifica se é admin
                login_view(request, user)
                return redirect('admin:index') #Redireciona para o painel de admin
            else:
                #Menssage de erro caso o usuário não seja admin
                messages.error(request, "Usuário não encontrado ou não autorizado.")
                return redirect('importar_funcionario')  #Redireciona de volta para o login de admin
        else:
            #Caso o login falhe
            messages.error(request, "Usuário ou senha inválidos")
            return render(request, 'funcionarios/login.html') 
    
    return render(request, 'funcionarios/login.html') #Renderiza a página de login


@login_required
@permission_required('funcionario.importar_funcionarios', raise_exception=True)
async def importar_funcionarios(request):
    #Formularios
    form_funcionario = FuncionarioForm()
    form_import = UploadExcelForm()

    tarefa_enfileirada = False #Variável para rastrear se a tarefa será enfileirada

    if request.method == 'POST':
        #Envio de dados manual
        if 'manual' in request.POST:  
            form_funcionario = FuncionarioForm(request.POST)
            if form_funcionario.is_valid():

                #Obtem o maior valor existente de cbo
                max_cbo = Funcionario.objects.aggregate(models.Max('cbo'))['cbo__max']
                next_cbo = max_cbo + 1 if max_cbo is not None else 1

                funcionario = form_funcionario.save(commit=False)
                funcionario.cbo = next_cbo #Atribui o próximo valor de cbo
                form_funcionario.save() #Salva o funcionario

                #Alteração para que o envio do email seja imediato quando se insere os dados dos funcionários via web
                #enviar_email_aniversario.apply_async()
                #queue.enqueue(enviar_email_aniversario)

                tarefa_enfileirada = True #Marca que a tarefa será enfileirada

                messages.success(request, "Funcinario adicionado com sucesso!")
                
                #Redireciona para a lista no admin após inserção manual
                return redirect('importar_funcionarios')
            
    
    #Se for envio de dados via arquivo excel
    if request.method == 'POST' and 'import' in request.POST and request.FILES.get('excel_file'):
        form_import = UploadExcelForm(request.POST, request.FILES)
        if form_import.is_valid():
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file)


                for _, row in df.iterrows():
                    #Obtem o maior valor existente de cbo
                    max_cbo = Funcionario.objects.aggregate(models.Max('cbo'))['cbo__max']
                    next_cbo = max_cbo +1 if max_cbo is not None else 1
                    
                    
                    Funcionario.objects.create(
                        nome=row['Nome'],
                        email=row['Email'],
                        data_nascimento=row['Data Nascimento'],
                        data_admissao=row['Data Admissão'],
                        funcao=row['Função'],
                        cbo=next_cbo #atribui o próximo valor de id sequencial
                    )

                tarefa_enfileirada = True #Marca que a tarefa será enfileirada

                messages.success(request, "Funcionarios importados com sucesso!")
                print("Funcionarios importados com sucesso!")
                
                #Redireciona para a lista no admin após importação
                # return redirect('admin:funcionarios_funcionario_changelist')
                return redirect('importar_funcionarios')

                #Chama a tarefa celery para envio de email de aniversario
                #enviar_email_aniversario.apply_async()
            
            except Exception as e:
                messages.error(request, f"Erro ao importar: {e}")
                print("Erro ao importar!")



    # ** Enfileira a tarefa após as operações de criação **
    if tarefa_enfileirada:
        enviar_email_aniversario.apply_async()

    return render(request, 'funcionarios/importar_funcionario.html', {
        'form_funcionario': form_funcionario,
        'form_import': form_import,
    })


def logout_and_redirect(request):
    logout(request)
    #return render (request, 'funcionarios/login.html') #esse caminho faz o caminho para o template login.html
    return redirect('login') #esse caminho faz o redirecionamento da url
