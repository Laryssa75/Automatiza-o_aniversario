from django.urls import path
from . import views

urlpatterns = [
    #exemplo de rota
    path('', views.home, name='home'),
    path('importar/', views.importar_funcionarios, name='importar_funcionarios'),
    path('logout/', views.logout_and_redirect, name='logout_and_redirect')
    path('enviar-email/', enviar_email_teste, name='enviar_email_teste'),
]