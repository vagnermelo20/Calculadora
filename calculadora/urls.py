# calculadora/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.CalculadoraView.as_view(), name='calculadora_main'),
    path('historico/deletar/', views.DeletarHistoricoView.as_view(), name='deletar_historico'),
]
