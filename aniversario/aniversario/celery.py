#Essa parte do código é onde ficará as configurações para os envio dos 
#emails usando a biblioteca celery

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

#Definindo o módulo Django para o Celery usar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aniversario.settings')

app = Celery('aniversario')

#Usando o Celery com o backend do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

#Carrega as tarefas de todos os aplicativos registrados
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# CELERY_BEAT_SCHEDULE = {
#     'enviar-emails-aniversariantes-diariamente':{
#         'task': 'funcionarios.tasks.enviar_emails_aniversariantes',
#         'schedule': crontab(hour=8, minute=0),
#     },
# }