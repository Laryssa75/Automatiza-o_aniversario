from django.core.management.base import BaseCommand
from funcionarios.models import Funcionario
from django.db import models

class Command(BaseCommand):
    help = 'Preenche os valores de cbo para funcionários existentes'

    def handle(self, *args, **kwargs):
        funcionario = Funcionario.objects.filter(cbo__isnull=True)
        next_cbo = Funcionario.objects.aaggregate(models.Max('cbo'))['cbo__max'] +1 if funcionario else 1

        for funcionario in funcionarios:
            funcionario.cbo = next_cbo
            funcionario.save()
            next_cbo += 1
        
        self.stdout.write(self.style.SUCCESS('Valores de cbo preenchidos com sucesso.'))