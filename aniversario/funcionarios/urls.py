from django.urls import path
from . import views

app_name = 'funcionarios'

urlpatterns = [
    #exemplo de rota
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('logout/', views.logout_and_redirect, name='logout_and_redirect'),
    path('cadastrar-funcionarios/', views.cadastrar_funcionarios, name='cadastrar_funcionarios'),
    path('editar-funcionarios/<int:cbo>/', views.editar_funcionarios, name='editar_funcionarios'),
    path('menu-cadastros/', views.menu_cadastros, name='menu_cadastros'),
    path('excluirfuncionario/<path:nome_funcionario>/', views.excluir_funcionario, name='excluir_funcionario'),
    #path('enviar-email-aniversariantes/', views.enviar_emails_aniversariantes_view, name='enviar_emails_aniversariantes'),
    path('admin/criar-usuario/', views.criar_usuario, name='criar_usuario'),
    path('admin/menu-usuarios/', views.menu_usuarios, name='menu_usuarios'),
    path('admin/excluir-usuario/<path:nome_usuario>/', views.excluir_usuario, name='excluir_usuario'),
    path('admin/editar-usuario/<int:id_usuario>/', views.editar_usuario, name='editar_usuario'),
    path('admin/salvar_permissoes/', views.salvar_permissoes, name='salvar_permissoes'),
]