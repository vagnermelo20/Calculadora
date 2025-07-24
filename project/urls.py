from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Inclui as rotas do app de usuário (home, login, cadastro, logout)
    path('', include('usuario.urls')), 
    
    # Inclui a rota do app da calculadora
    path('calculadora/', include('calculadora.urls')),
]