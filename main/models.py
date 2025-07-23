from django.db import models
from django.contrib.auth.hashers import make_password, check_password
'''Eu sei que o padrão do nome dos objetos são minusculos, mas eu coloquei maiusculo para seguir o padrão que me foi mandado de tabela'''

class Usuario(models.Model):
    IDUsuario = models.AutoField(primary_key=True)
    Nome = models.CharField(max_length=255, null=False, blank=False)
    Email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    Senha = models.CharField(max_length=128, null=False, blank=False)
    DtInclusao = models.DateTimeField(auto_now_add=True)

    '''Metodos para conseguir hashear e checar a senha hasheada'''
    def salvar_senha_hasheada(self, senha_nao_hash):
        self.Senha = make_password(senha_nao_hash)

    def checar_senha_hasheada(self, senha_nao_hash):
        return check_password(senha_nao_hash, self.Senha)

    def __str__(self):
        return f"{self.Nome} ({self.Email})"

    class Meta:
        # Formatar o nome de Usuario na tabela
        db_table = 'Usuario'
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

class Operacao(models.Model):
    IDOperacao = models.AutoField(primary_key=True)
    IDUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='IDUsuario')
    Parametros = models.CharField(max_length=255, null=False, blank=False)
    Resultado = models.CharField(max_length=255, null=False, blank=False)
    DtInclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Acessa o usuário através do campo IDUsuario dele e depois seu email, ai mostra os parametros e resultado
        return f"{self.IDUsuario.Nome} ({self.IDUsuario.Email})  equação: {self.Parametros} = {self.Resultado}"

    class Meta:
        # Formatar o nome de Operacao na tabela
        db_table = 'Operacao'
        verbose_name = "Operação"
        verbose_name_plural = "Operações"