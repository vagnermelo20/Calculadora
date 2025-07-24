# usuario/apps.py
from django.apps import AppConfig

class UsuarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuario'


    '''função criada para evitar o uso da função last_login do Django, bloqueando o update_last_login,
       que é o utilizado como padrão na função login do Django.'''
    def ready(self):
        from django.contrib.auth.signals import user_logged_in
        from django.contrib.auth.models import update_last_login

        user_logged_in.disconnect(
            update_last_login,
            dispatch_uid="update_last_login"
        )