#from celery import shared_task
from .models import Funcionario
from django.utils import timezone
from .email_utils import enviar
from django.core.mail import enviar
import logging
import django_rq

logger = logging.getLogger(__name__)

#@shared_task de uso apenas do celery
def enviar_email_aniversario():
    print("Tarefa executada no enviar email")
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

            #prepara os dados necessários para o envio do e-mail
            dados_envio = {
                "destinatario": funcionario.email,
                "nome_destinatario": funcionario.nome,
                "foto": funcionario.foto.path if funcionario.foto else None,
            }

            logger.info(f"Enviando e-mail para {funcionario.nome}")
            print(f"Enviando e-mail para {funcionario.nome}")

            sucesso = enviar(
                destinatario=dados_envio["destinatario"],
                nome_destinatario=dados_envio["nome_destinatario"],
                foto=dados_envio["foto"],
            )

            if sucesso:
                logger.info(f"E-mail enviado com sucesso para {funcionario.email}")
                print(f"E-mail enviado com sucesso para {funcionario.email}")
            else:
                logger.error(f"Falha ao enviar e-mail para {funcionario.email}")
                print(f"Falha ao enviar e-mail para {funcionario.email}")

        except Exception as e:
            logger.error(f"Erro ao enviar e-mail para {funcionario.nome}:  {str(e)}")
            print(f"Erro ao enviar e-mail para {funcionario.nome}:  {str(e)}")          






