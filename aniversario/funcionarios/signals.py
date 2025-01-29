from django.db.models.signals import post_migrate
from django.dispatch import receiver
from funcionarios.tasks import agenda_envio_email


@receiver(post_migrate)
def agendamento_envio(sender, **kwargs):
        if sender.label == 'funcionarios': #certifica de que é do app atual
            print("Sinal post_migrate foi disparado!")
            print(f"Post migrate signal received from: {sender}")
            print(f"additional kwargs: {kwargs}")
            agenda_envio_email()