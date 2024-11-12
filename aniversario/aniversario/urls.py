from django.contrib import admin
from django.urls import path, include
from funcionarios import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), #URL raiz, direcionando para view 'home' do app 'funcionarios'
    path('funcionarios/', include('funcionarios.urls')), #Urls do app funcionarios
]
