from django.db import models
from django.contrib.auth.hashers import make_password, check_password
'''nome padrao dos objetos em minusculo, mas coloquei maiusculo para enviar na tabela'''

class Usuario(models.Model):
    id_usuario  = models.AutoField(primary_key=True, db_column='IDUsuario')
    nome = models.CharField(max_length=255, null=False, blank=False, db_column='Nome')
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False, db_column='Email')
    senha = models.CharField(max_length=128, null=False, blank=False, db_column='Senha')
    dt_inclusao = models.DateTimeField(auto_now_add=True, db_column='DtInclusao')

    '''Metodos para conseguir hashear e checar a senha hasheada'''
    def salvar_senha_hasheada(self, senha_nao_hash):
        self.Senha = make_password(senha_nao_hash)

    def checar_senha_hasheada(self, senha_nao_hash):
        return check_password(senha_nao_hash, self.Senha)

    def __str__(self):
        return f"{self.nome} ({self.email})"

    class Meta:
        # Formatar o nome de Usuario na tabela
        db_table = 'Usuario'
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"