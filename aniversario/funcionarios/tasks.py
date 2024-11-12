from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from datetime import date
from .models import Funcionario
import logging
import yagmail

logger = logging.getLogger(__name__)

@shared_task
# def enviar_email_aniversario():
#     # Filtra funcionários com aniversários no dia atual
#     funcionarios = Funcionario.objects.filter(
#         data_nascimento__month=date.today().month,
#         data_nascimento__day=date.today().day
#     )
    
#     if not funcionario.exists():
#         logger.info("Nunhum aniversariante encontrado para o dia de hoje.")
#         print("Nenhuma anversariante encontrado para o dia de hoje.")

#     for funcionario in funcionarios:
#         try:
#             # Renderiza o template de email com os dados do funcionário
#             mensagem = render_to_string('funcionarios/email_template.html', {'funcionario': funcionario})
            
#             # Cria o objeto de email
#             email = EmailMessage(
#                 'Feliz Aniversário!',
#                 mensagem,
#                 'larissa@sooretama.net',
#                 [funcionario.email],
#             )

#             #Define o conteúdo como HTML
#             email.content_subtype = "html"

#             # Se o funcionário tiver uma foto, adiciona ao email
#             if funcionario.foto:
#                 email.attach_file(funcionario.foto.path)
            
#             # Envia o e-mail
#             email.send()
#             logging.info(f"Email enviado para {funcionario.email}")
#             print(f"Email enviado para {funcionario.email}")
        
#         except Exception as e:
#             #Log do erro, para verificar quais emails falharam
#             print(f"Erro ao enviar e-mail para {funcionario.email}: {e}")
#             logging.error(f"Erro ao enviar e-mail para {funcionario.email}: {e}")

def enviar_email_aniversario():
    try:
     # Configuração do yagmail
        yag = yagmail.SMTP('larissasoortama@gmail.com', 'yjmqrvdepyfunish')
        
        # Enviar e-mail para um destinatário de exemplo
        yag.send('larissa@sooretama.net', 'Assunto', 'Este é um e-mail de teste.')
        
        print("E-mail enviado com sucesso!")
    
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

    
