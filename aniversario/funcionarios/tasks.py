import logging
#from dramatiq.brokers.redis import RedisBroker
from datetime import timedelta
from .models import Funcionario
from django.utils import timezone
from .email_utils import enviar 
from celery import shared_task

logger = logging.getLogger(__name__)

# Configuração do broker e agendador do Dramatiq
# broker = RedisBroker("redis://localhost:6379")
# dramatiq.set_broker(broker)

@shared_task  #de uso apenas do celery
def enviar_email_aniversario():
    print("Tarefa executada no enviar email")
    logger.info("Tarefa executada no enviar email")
    
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

@shared_task
def agenda_envio_email():

    # Configura o próximo horário de execução
    proxima_execucao = timezone.now().replace(hour=16, minute=30, second=0, microsecond=0)
    if proxima_execucao < timezone.now():
        proxima_execucao += timedelta(days=1)

    #proxima_execucao = timezone.now()

    #Agenda a execução recorrente (a cada 24 horas)
    enviar_email_aniversario.apply_async(eta=proxima_execucao)

    logging.info(f"Tarefa de envio de email agendada para {proxima_execucao}")
    print(f"Tarefa de envio de eamil agendada para {proxima_execucao}")

