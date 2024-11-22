import pandas as pd
from django.shortcuts import render, redirect
from .models import Funcionario
from django.db import models
from django.contrib.auth import logout
from .forms import FuncionarioForm, UploadExcelForm
from django.contrib import messages
from django.http import JsonResponse
from .tasks import enviar_email_aniversario
from django.views.decorators.csrf import csrf_exempt


def enviar_emails_aniversariantes_view(request):

    enviar_email_aniversario().send()
    return JsonResponse({"status": "sucess", "message": "E-mails de aniversariantes enviados."})

def home(request):
    #return HttpResponse("Página inicial do app funcionários")
    return render(request, 'funcionarios/home.html')

@csrf_exempt  #caso queira permitir chamadas sem o token CSRF (apenas se necessario)
def importar_funcionarios(request):
    #Formulario de preenchimento manual e upload de arquivo
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
                return redirect('listar_funcionarios')
    
    #Se for envio de dados via arquivo excel
    if 'import' in request.method == 'POST' and request.FILES.get('excel_file'):
        form_import = UploadExcelForm(request.POST, request.FILES)
        if form_import.is_valid():
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file)

                #Obtem o maior valor existente de cbo
                max_cbo = Funcionario.objects.aggregate(models.Max('cbo'))['cbo__max']
                next_cbo = max_cbo +1 if max_cbo is not None else 1

                for _, row in df.iterrows():
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
                return redirect('listar_funcionarios')

                #Chama a tarefa celery para envio de email de aniversario
                #enviar_email_aniversario.apply_async()
                # queue.enqueue(enviar_email_aniversario)
            
            except Exception as e:
                messages.error(request, f"Erro ao importar: {e}")
                print("Erro ao importar!")



    # ** Enfileira a tarefa após as operações de criação **
    if tarefa_enfileirada:
        enviar_email_aniversario.send()

    return render(request, 'funcionarios/importar_excel.html', {
        'form_funcionario': form_funcionario,
        'form_import': form_import,
    })

def logout_and_redirect(request):
    logout(request)
    return redirect('admin:login')
