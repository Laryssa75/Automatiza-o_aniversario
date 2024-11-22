from django.apps import AppConfig

class FuncionariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'funcionarios'

    def ready(self):
        # Importa o Celery quando a aplicação for carregada
        #import aniversario.celery  # Isso importa o arquivo celery.py e inicializa o Celery

        from .tasks import agenda_envio_email
        agenda_envio_email()