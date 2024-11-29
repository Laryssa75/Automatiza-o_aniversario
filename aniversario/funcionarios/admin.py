from django.contrib import admin
from .models import Funcionario
from django.urls import path
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'data_nascimento', 'cbo', 'funcao', 'data_admissao')
    readonly_fields = ['cbo']

    #Adiciona uma ação personalizada no django admin
    actions = ['importar_excel']

    #Ação personalizada para importação
    def importar_funcionarios_acao(self, request, queryset):
        if not request.user.has_perm('funcionarios.permissao_importar_funcionarios'):
            raise PermissionDenied("Você não tem permissão")
        return HttpResponseRedirect('/importar_funcionarios')
    
    importar_funcionarios_acao.short_description = "Importar Funcionario"

    #Adicionar a ação do admin
    actions = ['importar_funcionarios_acao']

    #Sobrescrevendo as ações para verificar permissões 
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('funcionarios.permissao_importar_funcionarios'):
            actions.pop('importar_funcionarios_acoes', None)
        return actions
    
    #URLs personalizadas no admin
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('importar_funcionarios/', self.importar_funcionarios),
        ]
        return custom_urls + urls
    
    #Método para importar funcionarios
    def importar_funcionarios(self, request):
        if not request.user.has_perm('funcionarios.permissao_importar_funcionarios'):
            raise PermissionDenied("Você não tem permissão para acessar esta funcionalidade.")
        return HttpResponseRedirect('/importar_funcionarios/')
    
