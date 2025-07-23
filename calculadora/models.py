from django.db import models
from usuario.models import Usuario

'''Eu sei que o padrão do nome dos objetos são minusculos, mas eu coloquei maiusculo para seguir o padrão que me foi mandado de tabela'''

class Operacao(models.Model):
    IDOperacao = models.AutoField(primary_key=True)
    IDUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='IDUsuario')
    Parametros = models.CharField(max_length=255, null=False, blank=False)
    Resultado = models.CharField(max_length=255, null=False, blank=False)
    DtInclusao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.IDUsuario.Nome} ({self.IDUsuario.Email})  equação: {self.Parametros} = {self.Resultado}"

    class Meta:
        db_table = "Operacao"
        verbose_name = "Operação"
        verbose_name_plural = "Operações"
