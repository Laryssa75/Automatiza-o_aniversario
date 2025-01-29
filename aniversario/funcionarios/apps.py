from django.apps import AppConfig

class FuncionariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'funcionarios'

    def ready(self):
        #print("Executando o método read do FuncionarioConfig do apps.py")
        import funcionarios.signals

    