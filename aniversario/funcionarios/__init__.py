import os
import django

# Configura o Django para usar as configurações do projeto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aniversario.settings')

# Inicializa o Django
django.setup()
