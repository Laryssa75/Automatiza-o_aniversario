import logging
from celery.result import AsyncResult
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from funcionarios.models import Funcionario
from django.utils import timezone
from .email_utils import enviar 
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task(bind=True) #de uso apenas do celery
def enviar_email_aniversario(self):
    tarefa_id = self.request.id
    print(f"ID da tarefa: {tarefa_id}")

    print(f"Enviando e-mail para {funcionario.nome}. ID da tarefa: {tarefa_id}")

    # Filtra funcionários com aniversários no dia atual
    today = timezone.now().date()
    aniversariantes = Funcionario.objects.filter(
        data_nascimento__month= today.month,
        data_nascimento__day= today.day
    )

    logging.info(f"Buscando aniversariantes: {today}")
    print(f"Buscando aniversariantes: {today}")
    
    if not aniversariantes.exists():
        logging.info("Nunhum aniversariante encontrado para o dia de hoje.")
        print("Nenhuma anversariante encontrado para o dia de hoje.")
        return

    for funcionario in aniversariantes:
        try:
            #Verifica se a tarefa de envio de email já foi realizada
            if funcionario.id_tarefa_mail:
                logging.info(f"E-mail de aniversario já enviado para {funcionario.nome}. Tarefa ID: {funcionario.id_tarefa_mail}")        
                continue

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
                funcionario.id_tarefa_mail = tarefa_id
                funcionario.save()
                logger.info(f"E-mail enviado com sucesso para {funcionario.email}")
                print(f"E-mail enviado com sucesso para {funcionario.email}")
            else:
                logger.error(f"Falha ao enviar e-mail para {funcionario.email}")
                print(f"Falha ao enviar e-mail para {funcionario.email}")

        except Exception as e:
            logger.error(f"Erro ao enviar e-mail para {funcionario.nome}:  {str(e)}")
            print(f"Erro ao enviar e-mail para {funcionario.nome}:  {str(e)}")          


def check_agenda():
    try:
        funcionario = Funcionario.objects.filter(id_tarefa_mail__isnull=False).first()
        
        if not funcionario:  # Verifica se nenhum registro foi encontrado
            logging.info("Nenhuma tarefa registrada no momento.")
            print("Nenhuma tarefa registrada no momento.")
            return False

        tarefa_id = funcionario.id_tarefa_mail
    except Funcionario.DoesNotExist:
        logging.info("Erro ao buscar tarefas.")
        print("Erro ao buscar tarefas.")
        tarefa_id = None

    if tarefa_id:
        task_result = AsyncResult(tarefa_id)
        print(f"Verificando o status da tarefa: {task_result}")

        # Verifica se a tarefa já foi realizada, falhou ou está sendo executada
        if task_result.status not in ['PENDING', 'STARTED']:
            print(f"Task result status: {task_result.status}")
            logging.info(f"Tarefa ID {tarefa_id} já está em execução ou pendente.")
            return True  # Tarefa já está em execução ou agendada

    return False

@shared_task
def agenda_envio_email():

    # Configura o próximo horário de execução
    proxima_execucao = timezone.now().replace(hour=16, minute=35, second=0, microsecond=0)
    # if proxima_execucao < timezone.now():
    #     proxima_execucao += timedelta(days=1)

    #proxima_execucao = timezone.now()

    #Verifica se a tarefa já existe tarefa agendada
    if check_agenda():
        logging.info(f"Tarefa de envio de email agendada para {proxima_execucao}")
        return

    #Agenda a execução recorrente (a cada 24 horas)
    enviar_email_aniversario.apply_async(eta=proxima_execucao)

    logging.info(f"Tarefa de envio de email agendada para {proxima_execucao}")
    print(f"Tarefa de envio de email agendada para {proxima_execucao}")

