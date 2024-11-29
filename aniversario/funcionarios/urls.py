from django.urls import path
from . import views


urlpatterns = [
    #exemplo de rota
    path('login/', views.login, name='login'),
    path('', views.home, name='home'),
    path('importar-funcionarios/', views.importar_funcionarios, name='importar_funcionarios'),
    path('logout/', views.logout_and_redirect, name='logout_and_redirect'),
    #path('enviar-email-aniversariantes/', views.enviar_emails_aniversariantes_view, name='enviar_emails_aniversariantes'),
]