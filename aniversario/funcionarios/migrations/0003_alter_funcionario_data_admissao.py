# Generated by Django 5.1.3 on 2025-02-05 16:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0002_remove_usuariobasico_senha_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='data_admissao',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
