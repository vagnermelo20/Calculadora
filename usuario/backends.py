from django.contrib.auth.backends import ModelBackend
from .models import Usuario

'''Criei um backend de autenticação customizado para usar o modelo Usuario'''

class CustomAuthBackend(ModelBackend):
    """
    Autentica usando o model Usuario sem alterar a definição dele.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 'username' aqui é o email que a view passa
            user = Usuario.objects.get(email=username)
        except Usuario.DoesNotExist:
            return None

        # usa o método do próprio modelo para checar a senha
        if user.checar_senha_hasheada(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
