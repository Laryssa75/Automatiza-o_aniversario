import django_rq
from .tasks import enviar_email_aniversario

#Obtem a fila padrão
queue = django_rq.get_queue('default')

#Dados para enviar o e-mail
