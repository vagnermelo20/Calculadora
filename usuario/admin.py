from django.contrib import admin
from .models import Usuario
from .forms import UsuarioAdminForm 

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # --- Usa nosso formulário customizado ---
    form = UsuarioAdminForm

    # --- Configuração da Lista ---
    # (Isso continua igual)
    list_display = ('email', 'nome', 'dt_inclusao')
    search_fields = ('email', 'nome')
    list_filter = ('dt_inclusao',)
    ordering = ('-dt_inclusao',)

    # --- Configuração do Formulário de Edição/Criação ---
    # Agora, em vez de 'senha', usamos os campos do nosso formulário
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'email', 'senha1', 'senha2')
        }),
        ('Detalhes do Sistema', {
            'classes': ('collapse',),
            'fields': ('id_usuario', 'dt_inclusao')
        }),
    )
    
    # --- Campos Somente Leitura ---
    readonly_fields = ('id_usuario', 'dt_inclusao')