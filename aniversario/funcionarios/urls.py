from django.urls import path
from . import views


urlpatterns = [
    #exemplo de rota
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('logout/', views.logout_and_redirect, name='logout_and_redirect'),
    path('importar-funcionarios/', views.importar_funcionarios, name='importar_funcionarios'),
    path('editar-funcionario/<int:cbo>/', views.editar_funcionario, name='editar_funcionario'),
    path('menu-cadastros/', views.menu_cadastros, name='menu_cadastros'),
    #path('enviar-email-aniversariantes/', views.enviar_emails_aniversariantes_view, name='enviar_emails_aniversariantes'),
]