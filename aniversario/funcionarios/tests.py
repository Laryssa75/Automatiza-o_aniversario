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
from funcionarios.models import UsuarioBasico
user = UsuarioBasico.objects.criar_usuario(
    usuario='maria',
    senha_usuario='senha123',
    perfil = 'admin'
)
user.save()
print(f"Usuário {user.usuario} criado com sucesso!")

from funcionarios.models import UsuarioBasico
user = UsuarioBasico.objects.get(usuario='joana')
print(user.usuario, user.senha_usuario)

from funcionarios.models import UsuarioBasico
user = UsuarioBasico.objects.get(usuario='joana')
print(user.check_password('senha123'))

from funcionarios.models import UsuarioBasico

# Usando o método do GerenciadorUsuarios para criar um usuário básico
usuario = UsuarioBasico.objects.criar_usuario(usuario='andre', password='senha123', perfil='basico', setor='TI')


#mudando o tipo de acesso de um usuario basico para admin
from funcionarios.models import UsuarioBasico
from django.contrib.auth.hashers import make_password

usuario = UsuarioBasico(
    usuario = "sabrina",
    perfil = "admin",
    setor = "adm"
)
usuario.password = make_password("senha123")
usuario.save()
if usuario.check_password("senha123"):
    print("senha correta")
else:
    print("senha errada")

usuario.save()
usuario = Usuario.objects.get(usuario="leticia")
print(usuario.perfil)
print(usuario.usuario)
print(usuario.senha_usuario)


usuario.senha_usuario = ("senha123")
usuario.save()
usuario = Usuario.objects.get(usuario="leticia")
print(usuario.perfil)

print(f"{usuario.usuario} {usuario.perfil} modificil perfil:{usuario.perfil} e senha{usuario.senha_usuario}")

#mostrar todos os usuarios que estao dentro do banco
from funcionarios.models import Usuario
usuarios = Usuario.objects.all()
for usuario in usuarios:
    print(usuario)

from funcionarios.models import Usuario

# Verifica se o usuário existe
usuario = Usuario.objects.filter(usuario="leticia").first()

if usuario is not None:
    if usuario.perfil == 'admin':
        print(f"Usuário {usuario.usuario} tem acesso administrativo.")
    else:
        print(f"Usuário {usuario.usuario} tem acesso básico.")
else:
    print("Usuário não encontrado.")



#concedendo permissao de um função especifica para um usuário via shell
from django.contrib.auth.models import User, Permission

# Encontre o usuário
user = User.objects.get(username='maria')

# Encontre a permissão personalizada
permission = Permission.objects.get(codename='cadastrar_funcionarios')

# Atribua a permissão
user.user_permissions.add(permission)
user.save()

#Verificando se a permissão foi concedida
if user.has_perm('funcionarios.cadastrar_funcionarios'):
    print("Usuário tem permissão")
else:
    print("Usuário NÃO tem permissão")


#permissões disponiveis para verificar via shell
from django.contrib.auth.models import Permission

permissions = Permission.objects.all()
for perm in permissions:
    print(perm.codename)


from funcionarios.models import Funcionario

# Filtrar registros com data_nascimento nulo
funcionarios_com_null = Funcionario.objects.filter(data_nascimento__isnull=True)
print(f"Funcionarios com data nascimento nula: {funcionarios_com_null}")

# Atualizar manualmente os valores
for funcionario in funcionarios_com_null:
    funcionario.data_nascimento = '2000-01-01'  # Ou outro valor padrão
    funcionario.save()

from funcionarios.models import Funcionario
from funcionarios.utils import obter_proximo_cbo, reorganizar_cbo

# Testa o próximo CBO
proximo_cbo = obter_proximo_cbo()
print("Próximo CBO disponível:", proximo_cbo)

# Reorganiza os CBOs
reorganizar_cbo()
print("CBOs reorganizados com sucesso.")

#Verificar as permissões que o usuário tem
# Abrir o shell
python manage.py shell

# Importar os modelos
from django.contrib.auth.models import User

# Obter o usuário
user = User.objects.get(username='maria')

# Verificar se tem permissão
tem_permissao = user.has_perm('funcionarios.cadastrar_funcionarios')
print(tem_permissao)

from django.contrib.auth.models import Permission

# Listar as permissões associadas à app 'funcionarios'
permissions = Permission.objects.filter(content_type__app_label='funcionarios')
for perm in permissions:
    print(perm.codename)  # Vai exibir o codename das permissões

<!-- CBO -->
                <div class="mb-4">
                    <label for="{{ form_funcionario.cbo.id_for_label }}" class="form-label">CBO</label>
                    <h4 class="form-label fw-normal">{{ cbo_gerado }}</h4>
                    <input 
                        type="hidden" 
                        name="cbo"
                        class="form-control"
                        value="{{ cbo_gerado }}">
                    {% if form_funcionario.cbo.errors %}
                    <div class="text-danger small">
                        {{ form_funcionario.cbo.errors }}
                    </div>
                    {% endif %}
                </div>