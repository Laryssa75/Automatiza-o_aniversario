from celery import shared_task
from .models import Funcionario
from django.utils import timezone
from .email_utils import enviar
import logging

logger = logging.getLogger(__name__)

@shared_task
def enviar_email_aniversario():
    # Filtra funcionários com aniversários no dia atual
    today = timezone.now().date()
    aniversariantes = Funcionario.objects.filter(
        data_nascimento__month= today.month,
        data_nascimento__day= today.day
    )
    
    if not funcionario.exists():
        logger.info("Nunhum aniversariante encontrado para o dia de hoje.")
        print("Nenhuma anversariante encontrado para o dia de hoje.")

    for funcionario in aniversariantes:
  

        enviar(destinatario=funcionario.email, nome_destinatario=funcionario.nome)
        print(f"Envio do email{funcionario.email}, enviado com sucesso.")
           
# def enviar_email_aniversario():
#     try:
#      # Configuração do yagmail
#         yag = yagmail.SMTP('larissasoortama@gmail.com', 'yjmqrvdepyfunish')
        
#         # Enviar e-mail para um destinatário de exemplo
#         yag.send('larissa@sooretama.net', 'Assunto', 'Este é um e-mail de teste.')
        
#         print("E-mail enviado com sucesso!")
    
#     except Exception as e:
#         print(f"Erro ao enviar e-mail: {e}")

    
