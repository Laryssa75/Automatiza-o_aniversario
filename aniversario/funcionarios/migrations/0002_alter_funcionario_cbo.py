# Generated by Django 5.1.3 on 2024-11-19 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='cbo',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
