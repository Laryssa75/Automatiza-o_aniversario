import pandas as pd
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import authenticate, login 
from django.shortcuts import render, redirect
from .models import Funcionario
from django.db import models
from django.contrib.auth import logout
from .forms import FuncionarioForm, UploadExcelForm
from django.contrib import messages
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


@login_required
@permission_required('funcionarios.importar_funcionarios', raise_exception=True)
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

                messages.success(request, "Funcionário adicionado com sucesso!")

                #Alteração para que o envio do email seja imediato quando se insere os dados dos funcionários via web
                #enviar_email_aniversario.apply_async()
                #queue.enqueue(enviar_email_aniversario)

                tarefa_enfileirada = True #Marca que a tarefa será enfileirada

                messages.success(request, "Funcinario adicionado com sucesso!")
                
                #Redireciona para a lista no admin após inserção manual
                return redirect('importar_funcionarios')
            
            else:
                messages.error(request, "Erro ao adicionar funcionário.")
            
    
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
