from django.test import TestCase

# Create your tests here.

#Testes do resultado via shell

from celery.result import AsyncResult

# Substitua pelo ID da tarefa retornada
resultado = AsyncResult('a9ef6da8-5715-406b-b9da-ac8934d1d7fd')

# Verifique o status
print(resultado.status)  # Deve ser 'SUCCESS' se a tarefa foi concluída com sucesso
print(resultado.result)   # Exibe o resultado ou a exceção, se houver


# PENDING: A tarefa ainda não foi executada.
# STARTED: A tarefa foi iniciada, mas ainda não foi concluída.
# SUCCESS: A tarefa foi executada com sucesso.
# FAILURE: A tarefa falhou, normalmente seguido de um traceback.

from funcionarios.tasks import agenda_envio_email
agenda_envio_email.apply()