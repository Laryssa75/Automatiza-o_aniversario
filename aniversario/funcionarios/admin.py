from django.contrib import admin
from .models import Funcionario

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'data_nascimento')
    #list_display = ('nome', 'email', 'data_nascimento', 'cbo', 'data_admissao', 'cargo')

