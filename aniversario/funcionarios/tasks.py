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

    logger.info(f"Buscando aniversariantes: {today}")
    print(f"Buscando aniversariantes: {today}")
    
    if not aniversariantes.exists():
        logger.info("Nunhum aniversariante encontrado para o dia de hoje.")
        print("Nenhuma anversariante encontrado para o dia de hoje.")
        return

    for funcionario in aniversariantes:
        try:
            logger.info(f"Enviando e-mail para {funcionario.nome}")
            print(f"Enviando e-mail para {funcionario.nome}")

            enviar(destinatario=funcionario.email, nome_destinatario=funcionario.nome, foto = None)
            
            print(f"Envio do email{funcionario.email}, enviado com sucesso.")
            logger.info(f"Envio de e-mail {funcionario.email}, enviado com sucesso") 

        except Exception as e:
            logger.error(f"Erro ao enviar e-mail para {funcionario.nome}:  {str(e)}")
            print(f"Erro ao enviar e-mail para {funcionario.nome}:  {str(e)}")          

    
