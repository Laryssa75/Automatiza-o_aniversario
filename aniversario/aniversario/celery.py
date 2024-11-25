#Essa parte do código é onde ficará as configurações para os envio dos 
#emails usando a biblioteca celery

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
#from celery.schedules import crontab


#Definindo o módulo Django para o Celery usar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aniversario.settings')

app = Celery('aniversario')

# Configuração do fuso horário
app.conf.timezone = 'America/Sao_Paulo'

#Usando o Celery com o backend do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

#Carrega as tarefas de todos os aplicativos registrados
app.autodiscover_tasks()

#print("Tarefas disponiveis:", app.tasks)


#Configurando o celery beat para rodar a tarefa todoso os dias
# app.conf.beat_schedule = {
#     'enviar-email-diariamente': {
#         'task': 'funcionarios.tasks.enviar_email_aniversario',  # Referência para sua função Celery
#         'schedule': crontab(minute=15, hour=18),  # Executa todos os dias às 18:15
#     },
# }

app.conf.broker_connection_retry_on_startup = True


#Útil para teste e depuração de código
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
