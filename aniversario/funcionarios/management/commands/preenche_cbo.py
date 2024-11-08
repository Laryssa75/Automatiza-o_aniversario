from django.core.management.base import BaseCommand
from funcionarios.models import Funcionario
from django.db.models import Max

class Command(BaseCommand):
    help = 'Preenche os valores de cbo para funcionários existentes'

    def handle(self, *args, **kwargs):
        funcionario = Funcionario.objects.filter(cbo__isnull=True)
        max_cbo = Funcionario.objects.aggregate(Max('cbo'))['cbo__max']
        max_cbo = max_cbo +1 if max_cbo is not None else 0

        for funcionario in Funcionario.objects.filter(cbo__isnull=True):
            funcionario.cbo = next_cbo
            funcionario.save()
            next_cbo = max_cbo + 1
        
        self.stdout.write(self.style.SUCCESS('Valores de cbo preenchidos com sucesso.'))