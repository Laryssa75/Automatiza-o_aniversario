# Generated by Django 5.1.3 on 2025-01-16 12:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0008_alter_funcionario_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('usuario', models.CharField(help_text='Digite um nome de usuário alfanumérico.', max_length=100, validators=[django.core.validators.RegexValidator(message='Este campo deve conter apenas letras e números.', regex='^[a-zA-Z0-9]*$')])),
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('senha_usuario', models.CharField(help_text='Crie uma senha alfanumérica.', max_length=20, validators=[django.core.validators.RegexValidator(message='Este campo deve conter apenas letras e números.', regex='^[a-zA-Z0-9]*$')])),
                ('perfil', models.CharField(choices=[('admin', 'Administrador'), ('basico', 'Básico')], default='basico', max_length=50)),
                ('setor', models.CharField(max_length=100)),
                ('data_criarUsu', models.DateField(blank=True, null=True)),
            ],
        ),
    ]