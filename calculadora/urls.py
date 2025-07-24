from django.urls import path
from . import views
urlpatterns = [
    # A rota principal do app da calculadora
    path('', views.CalculadoraView.as_view(), name='calculadora_main'),
]

