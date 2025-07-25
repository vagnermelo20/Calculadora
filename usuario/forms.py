from django import forms
from .models import Usuario

class UsuarioAdminForm(forms.ModelForm):
    """Um formulário simples para criar e editar usuários no admin."""

    # Campo para a nova senha
    senha1 = forms.CharField(
        label='Nova Senha', 
        widget=forms.PasswordInput, 
        required=False, # Não é obrigatório ao editar
        help_text='Deixe em branco para não alterar a senha.'
    )
    # Campo para confirmar a nova senha
    senha2 = forms.CharField(
        label='Confirmação da Senha', 
        widget=forms.PasswordInput, 
        required=False
    )

    class Meta:
        model = Usuario
        fields = ('email', 'nome') 

    def clean(self):
        """
        Método de validação para o formulário inteiro.
        """
        cleaned_data = super().clean()
        senha1 = cleaned_data.get("senha1")
        senha2 = cleaned_data.get("senha2")

        # Se o usuário está sendo criado, a senha é obrigatória
        if not self.instance.pk and not senha1:
            raise forms.ValidationError("Para criar um novo usuário, você precisa definir uma senha.")

        # Se as senhas foram preenchidas, verifica se são iguais
        if senha1 and senha1 != senha2:
            raise forms.ValidationError("As senhas não coincidem.")
        
        return cleaned_data

    def save(self, commit=True):
        """
        Sobrescreve o método save para lidar com a senha.
        """
        # Pega a instância do usuário, mas não salva ainda (commit=False)
        usuario = super().save(commit=False)
        
        nova_senha = self.cleaned_data.get("senha1")
        if nova_senha:
            # Se uma nova senha foi fornecida, usa nosso método para hashear
            usuario.salvar_senha_hasheada(nova_senha)

        if commit:
            usuario.save() # Salva a instância no banco

        return usuario