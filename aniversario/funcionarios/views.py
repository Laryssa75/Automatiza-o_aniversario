import pandas as pd
import yagmail
from django.shortcuts import render, redirect
from .models import Funcionario
from django.db import models
from .tasks import enviar_email_aniversario
from django.http import HttpResponse
from django.contrib.auth import logout
from .forms import FuncionarioForm, UploadExcelForm
from django.contrib import messages
from django.http import JsonResponse
from .tasks import enviar_email_aniversario

def enviar_email_teste(request):
    try:
        #configurando o yagmail
        yag = yagmail.SMTP('larissasooretama@gmail.com', 'yjmqrvdepyfunish')

        #enviar email
        yag.send('larissa@sooretama.net', 'Assunto', 'Este é um email teste')

        return HttpResponse("Email enviado com sucesso!")
    except Exception as e:
        return HttpResponse(f"Erro ao enviar email {e}")


def home(request):
    #return HttpResponse("Página inicial do app funcionários")
    return render(request, 'funcionarios/home.html')

def importar_funcionarios(request):
    #Formulario de preenchimento manual e upload de arquivo
    form_funcionario = FuncionarioForm()
    form_import = UploadExcelForm()

    if request.method == 'POST':
        if 'manual' in request.POST:  #Envio de dados manual
            form_funcionario = FuncionarioForm(request.POST)
            if form_funcionario.is_valid():
                form_funcionario.save()
                messages.success(request, "Funcinario adicionado com sucesso!")
                return redirect('listar_funcionarios')
    
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

                    next_cbo += 1 #incrementa para o próximo registro

                messages.success(request, "Funcionarios importados com sucesso!")
                print("Funcionarios importados com sucesso!")
                #Chama a tarefa celery para envio de email de aniversario
                enviar_email_aniversario.apply_async()
                return redirect('listar_funcionarios')
            except Exception as e:
                messages.error(request, f"Erro ao importar: {e}")
                print("Erro ao importar!")

    return render(request, 'funcionarios/importar_excel.html', {
        'form_funcionario': form_funcionario,
        'form_import': form_import
    })

def logout_and_redirect(request):
    logout(request)
    return redirect('admin:login')

def enviar_emails_aniversariantes_view(request):
    enviar_email_aniversario.delay() #Executa a tarefa em background com Celery
    return JsonResponse({"status": "sucess", "message": "E-mails de aniversariantes enviados."})