from django.db.models.signals import pre_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from funcionarios.tasks import agenda_envio_email
from .models import Usuario

@receiver(pre_save, sender=Usuario)
def criptografar_senha(sender, instance, **kwargs):
    print("sinal pre_save disparado!")
    print(f"Sender: {sender}")
    print(f"Instance: {instance}")
    print(f"kwargs: {kwargs}")

    if not instance.pk:
        print("Novo usuário sendo criado!")
    else:
        print(f"Usuário {instance.pk} já existe.")
    
    if not instance.pk:
        instance.senha_usuario = make_password(instance.senha_usuario)
        print(f"Senha criptografada: {instance.senha_usuario}")


@receiver(post_migrate)
def agendamento_envio(sender, **kwargs):
        if sender.label == 'funcionarios': #certifica de que é do app atual
            print("Sinal post_migrate foi disparado!")
            print(f"Post migrate signal received from: {sender}")
            print(f"additional kwargs: {kwargs}")
            agenda_envio_email()