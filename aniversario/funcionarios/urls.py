from django.urls import path
from . import views

urlpatterns = [
    #exemplo de rota
    path('', views.index, name='index'),
    path('importar/', views.importar_funcionarios, name='importar_funcionarios'),
]