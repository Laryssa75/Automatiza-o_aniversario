# Generated by Django 5.1.3 on 2024-12-17 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0005_remove_funcionario_id_alter_funcionario_cbo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='data_nascimento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
