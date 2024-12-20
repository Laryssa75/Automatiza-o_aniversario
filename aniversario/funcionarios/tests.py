from django.test import TestCase

# Create your tests here.

#Testes do resultado via shell

from celery.result import AsyncResult

# Substitua pelo ID da tarefa retornada
resultado = AsyncResult('bd970a13-98e6-4dd1-a7f4-3206b2ad3078')

# Verifique o status
print(resultado.status)  # Deve ser 'SUCCESS' se a tarefa foi concluída com sucesso
print(resultado.result)   # Exibe o resultado ou a exceção, se houver


# PENDING: A tarefa ainda não foi executada.
# STARTED: A tarefa foi iniciada, mas ainda não foi concluída.
# SUCCESS: A tarefa foi executada com sucesso.
# FAILURE: A tarefa falhou, normalmente seguido de um traceback.

from funcionarios.tasks import agenda_envio_email
agenda_envio_email.apply()

from django.core.mail import send_mail

send_mail(
    'Teste de E-mail',
    'Mensagem de teste.',
    'larissa@sooretama.net',
    ['larissa@sooretama.net'],
    fail_silently=False,
)

#celery -A aniversario inspect scheduled

from celery.app.control import Inspect
from aniversario.celery import aniversario

inspect = Inspect(app=aniversario)
scheduled_tasks = inspect.scheduled()

print(scheduled_tasks)

from funcionarios.email_utils import enviar
from funcionarios.tasks import enviar_email

# Testar o envio para um dos aniversariantes
dados_envio = {
    "destinatario": "larissa@sooretama.net",  # Substitua pelo e-mail real
    "nome_destinatario": "João Carvalho",
    "foto": None,  # Substitua pelo caminho da foto se necessário
}

sucesso = enviar_email(
    destinatario=dados_envio["destinatario"],
    nome_destinatario=dados_envio["nome_destinatario"],
    foto=dados_envio["foto"],
)

print("Sucesso no envio:", sucesso)

#para saber se o broker está ativo
from celery.app.control import Inspect
from aniversario.celery import app as aniversario

# Inspecionar os workers ativos
inspect = Inspect(app=aniversario)
active_workers = inspect.active()

print("Workers ativos:")
print(active_workers)


from funcionarios.tasks import enviar

# Substitua pelos dados reais de teste
destinatario = "larissa@sooretama.net"
assunto = "Teste de E-mail"
mensagem = "Este é um teste de envio de e-mail via Celery."
foto= "None"

# Testa a função diretamente
enviar(destinatario, assunto, mensagem, foto)

from funcionarios.tasks import enviar_email_aniversario

enviar_email_aniversario.apply()


#criando um login de usuário normal válido
from django.contrib.auth.models import User
user = User.objects.create_user(
    username='maria',
    password='senha123',
    email='larissa@sooretama.net'
)

user.save()

print("Usuário craido com sucesso!")

#concedendo permissao de um função especifica para um usuário via shell
from django.contrib.auth.models import User, Permission

# Encontre o usuário
user = User.objects.get(username='maria')

# Encontre a permissão personalizada
permission = Permission.objects.get(codename='importar_funcionarios')

# Atribua a permissão
user.user_permissions.add(permission)
user.save()

#Verificando se a permissão foi concedida
if user.has_perm('funcionarios.importar_funcionarios'):
    print("Usuário tem permissão")
else:
    print("Usuário NÃO tem permissão")


#permissões disponiveis para verificar via shell
from django.contrib.auth.models import Permission

permissions = Permission.objects.all()
for perm in permissions:
    print(perm.codename)

