from django.urls import path
from . import views


urlpatterns = [
    #exemplo de rota
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('logout/', views.logout_and_redirect, name='logout_and_redirect'),
    path('importar-funcionarios/', views.importar_funcionarios, name='importar_funcionarios'),
    path('editar-funcionarios/<int:cbo>/', views.editar_funcionarios, name='editar_funcionarios'),
    path('menu-cadastros/', views.menu_cadastros, name='menu_cadastros'),
    path('excluir-cadastro/<int:cbo>/', views.excluir_funcionario, name='excluir_funcionario'),
    #path('enviar-email-aniversariantes/', views.enviar_emails_aniversariantes_view, name='enviar_emails_aniversariantes'),
]