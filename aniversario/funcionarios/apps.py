from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class FuncionariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'funcionarios'

    def ready(self):
        #conectar o sinal post_migrate para executar após a inicialização
        post_migrate.connect(self.agendamento_envio, sender=self)

    @receiver(post_migrate, sender='funcionarios')
    def agendamento_envio(self, sender, **kwargs):
        print("Sinal post_migrate foi disparado!")
        print(f"Post migrate signal received from: {sender}")
        print(f"additional kwargs: {kwargs}")
        from .tasks import agenda_envio_email
        agenda_envio_email()