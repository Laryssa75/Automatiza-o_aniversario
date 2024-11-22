import os
import sys
from enviar_email import iniciar_tarefa

def main():
    """Rodar tarefas administrativas do Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agendamento_aniversario.settings')
    
    # Iniciar o agendador de tarefas
    iniciar_tarefa()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
