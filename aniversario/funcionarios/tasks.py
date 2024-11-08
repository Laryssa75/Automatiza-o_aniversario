from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from datetime import date
from .models import Funcionario

@shared_task
def enviar_email_aniversario():
    # Filtra funcionários com aniversários no dia atual
    funcionarios = Funcionario.objects.filter(
        data_nascimento__month=date.today().month,
        data_nascimento__day=date.today().day
    )

    for funcionario in funcionarios:
        # Renderiza o template de email com os dados do funcionário
        mensagem = render_to_string('funcionarios/email_template.html', {'funcionario': funcionario})
        
        # Cria o objeto de email
        email = EmailMessage(
            'Feliz Aniversário!',
            mensagem,
            'larissa@sooretama.net',
            [funcionario.email],
        )

        # Se o funcionário tiver uma foto, adiciona ao email
        if funcionario.foto:
            email.attach_file(funcionario.foto.path)
        
        # Envia o e-mail
        email.send()
