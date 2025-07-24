from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class CalculadoraView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'calculadora/calculadora.html')