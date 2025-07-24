from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth import login, logout, authenticate
from .models import Usuario

class HomeView(View):
    def get(self, request):
        return render(request, 'usuario/home.html')
    
class CadastroView(View):
    def get(self, request):
        return render(request, 'usuario/cadastro.html')

    def post(self, request):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_confirmacao = request.POST.get('senha_confirmacao')

        if senha != senha_confirmacao:
            context = {'error': 'As senhas não coincidem!'}
            return render(request, 'usuario/cadastro.html', context)

        if Usuario.objects.filter(email=email).exists():
            context = {'error': 'Este email já está em uso.'}
            return render(request, 'usuario/cadastro.html', context)

        user = Usuario(nome=nome, email=email)
        user.salvar_senha_hasheada(senha)
        user.save()
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'usuario/login.html')

    def post(self, request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user = authenticate(request, username=email, password=senha)

        if user is not None:
            login(request, user)  # já sem update_last_login para Usuario
            return redirect('calculadora_main')

        return render(request, 'usuario/login.html', {
            'error': 'Email ou senha inválidos.'
        })

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')