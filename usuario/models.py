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