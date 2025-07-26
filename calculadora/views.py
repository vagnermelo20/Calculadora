# calculadora/views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Operacao
import re

class Calculadora:
    """
    Versão final e correta da calculadora, com suporte a parênteses
    e tratamento correto de números negativos.
    """
    def _tokenizar(self, expressao_str):
        """Fatia a string em uma lista de números e operadores."""
        if not expressao_str: return []
        # A expressão regular encontra números (incluindo negativos no início) ou operadores/parênteses.
        tokens_str = re.findall(r'-?\d+\.?\d*|[+\-*/()]', expressao_str)
        tokens_processados = []
        for t in tokens_str:
            try:
                tokens_processados.append(float(t))
            except ValueError:
                tokens_processados.append(t)
        return tokens_processados

    def _resolver_expressao_simples(self, tokens):
        """
        Recebe uma lista de tokens SEM parênteses e a resolve,
        respeitando a ordem das operações.
        """
        # 1º Passe: Multiplicação e Divisão
        i = 0
        while i < len(tokens):
            if tokens[i] == '*':
                resultado = tokens[i-1] * tokens[i+1]
                tokens[i-1:i+2] = [resultado]
                i = 0 # Reinicia o loop
            elif tokens[i] == '/':
                if tokens[i+1] == 0: raise ValueError("Divisão por zero")
                resultado = tokens[i-1] / tokens[i+1]
                tokens[i-1:i+2] = [resultado]
                i = 0 # Reinicia o loop
            else:
                i += 1
        
        # 2º Passe: Soma e Subtração
        i = 0
        while i < len(tokens):
            if tokens[i] == '+':
                resultado = tokens[i-1] + tokens[i+1]
                tokens[i-1:i+2] = [resultado]
                i = 0 # Reinicia o loop
            elif tokens[i] == '-':
                # Se for o primeiro item, trata como número negativo
                if i == 0:
                    tokens[i+1] = -tokens[i+1]
                    tokens.pop(0)
                else:
                    resultado = tokens[i-1] - tokens[i+1]
                    tokens[i-1:i+2] = [resultado]
                i = 0 # Reinicia o loop
            else:
                i += 1
        
        return tokens[0]

    def calcular(self, expressao_str):
        """
        O método principal que resolve a expressão completa,
        incluindo os parênteses.
        """
        expressao = expressao_str.replace(" ", "")

        # Loop para resolver os parênteses de dentro para fora
        while '(' in expressao:
            inicio = expressao.rfind('(')
            fim = expressao.find(')', inicio)
            if inicio == -1 or fim == -1: raise ValueError("Parênteses não balanceados")
            
            sub_expressao = expressao[inicio+1:fim]
            sub_tokens = self._tokenizar(sub_expressao)
            
            resultado_sub = self._resolver_expressao_simples(sub_tokens)
            
            # Substitui a expressão com parênteses (ex: "(-9)") pelo seu resultado (ex: "-9.0")
            expressao = expressao[:inicio] + str(resultado_sub) + expressao[fim+1:]

        # Calcula a expressão final, já sem parênteses
        tokens_finais = self._tokenizar(expressao)
        resultado_final = self._resolver_expressao_simples(tokens_finais)

        # Arredonda para evitar dízimas longas e formata para inteiro se aplicável
        resultado_arredondado = round(resultado_final, 10)
        return int(resultado_arredondado) if resultado_arredondado == int(resultado_arredondado) else resultado_arredondado


class CalculadoraView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        operacoes = Operacao.objects.filter(IDUsuario=request.user).order_by('-DtInclusao')[:10]
        context = {'historico': operacoes}
        return render(request, 'calculadora/calculadora.html', context)

    def post(self, request):
        expressao = request.POST.get('display', '')
        resultado_final = None
        erro_calculo = None

        try:
            # --- CHAMADA CORRIGIDA ---
            # 1. Cria uma instância vazia da calculadora
            calculadora = Calculadora()
            # 2. Chama o método 'calcular', passando a expressão
            resultado_final = calculadora.calcular(expressao)
            
        except (ValueError, IndexError) as e:
            # Captura qualquer erro de cálculo ou de formato da expressão
            erro_calculo = str(e) if str(e) else "Expressão inválida."
        
        # O resto da view continua igual...
        operacoes = Operacao.objects.filter(IDUsuario=request.user).order_by('-DtInclusao')[:10]
        context = {
            'historico': operacoes,
            'expressao_atual': expressao,
        }
        if erro_calculo:
            context['erro'] = erro_calculo
            context['resultado_atual'] = ''
        else:
            Operacao.objects.create(
                IDUsuario=request.user,
                Parametros=expressao,
                Resultado=str(resultado_final)
            )
            context['historico'] = Operacao.objects.filter(IDUsuario=request.user).order_by('-DtInclusao')[:10]
            context['resultado_atual'] = resultado_final
        return render(request, 'calculadora/calculadora.html', context)


class DeletarHistoricoView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request):
        Operacao.objects.filter(IDUsuario=request.user).delete()
        return redirect('calculadora_main')