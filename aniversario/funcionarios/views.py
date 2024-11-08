from django.http import HttpResponse
import pandas as pd
from django.shortcuts import render, redirect
from .models import Funcionario
from django.db import models
from .tasks import enviar_email_aniversario

# Create your views here.
def index(request):
    return HttpResponse("Página inicial do app funcionários")

def importar_funcionarios(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        #Obtem o maior valor existente de cbo
        max_cbo = Funcionario.objects.aaggregate(models.Max('cbo'))['cbo__max']
        next_cbo = max_cbo +1 if max_cbo is not None else 1

        for _, row in df.interrows():
            Funcionario.objects.create(
                nome=row['Nome'],
                email=row['Email'],
                data_nascimento=row['Data Nascimento'],
                data_admissao=row['Data Admissão'],
                funcao=row['Função'],
                cbo=next_cbo #atribui o próximo valor de id sequencial
            )

            next_cbo += 1 #incrementa para o próximo registro

        #Chama a tarefa celery para envio de email de aniversario
        enviar_email_aniversario.apply_async()

        return redirect('listar_funcionarios')
    return render(request, 'funcionarios/importar_excel.html')