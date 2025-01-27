from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from apps.tech_assets.models import *

# Register your models here.


class ListingUsers(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'mostrar_grupo',
                    'is_superuser', 'mostrar_data_add', 'mostrar_data_change',)
    list_display_links = ('id', 'username')

    # Aqui personaliza que na página de admin no formulário de usuário não pode ser alterada a informação de data de registo
    readonly_fields = ('date_joined', 'last_login')

    def mostrar_grupo(self, user):
        obj = Group.objects.filter(user=user.id)
        if obj:
            grupos = ', '.join([x.name for x in obj][0:2])
            # Por questão de adequação, vamos listar na tela inicial somente até 3 grupos, caso haja mais, concatena um ...
            if len([x.name for x in obj]) > 3:
                return grupos + ', ...'
            else:
                return grupos
        else:
            return '-'
    mostrar_grupo.short_description = 'Grupos'

    '''    def mostrar_data_add(self, obj):
        # Buscando na tabela django_content_type o ID que o Model do Objeto obteve quando criado
        content_type_id = ContentType.objects.get_for_model(obj.__class__)

        # Com o content_type_id em mãos, agora conseguimos obter a data de criação do objeto especifico (registro especifico) para lista-lo
        log_entries = LogEntry.objects.filter(
            object_id=obj.id, content_type=content_type_id, action_flag=ADDITION)

        # Verifica se existe essa informação e retorna ela, caso contrário não retorna nada
        if log_entries.exists():
            return log_entries.first().action_time
        return None
    # dando nome a coluna do list_display que irá mostrar essa informação
    mostrar_data_add.short_description = 'Data Inclusão'''

    def mostrar_data_add(self, obj):
        return User.objects.get(id=obj.id).date_joined
    # dando nome a coluna do list_display que irá mostrar essa informação
    mostrar_data_add.short_description = 'Data Inclusão'

    def mostrar_data_change(self, obj):
        # Buscando na tabela django_content_type o ID que o Model do Objeto obteve quando alterado
        content_type_id = ContentType.objects.get_for_model(obj.__class__)

        # Com o content_type_id em mãos, agora conseguimos obter a data de alteração do objeto especifico (registro especifico) para lista-lo
        log_entries = LogEntry.objects.filter(
            object_id=obj.id, content_type=content_type_id, action_flag=CHANGE)

        # Verifica se existe essa informação e retorna ela, caso contrário não retorna nada
        if log_entries.exists():
            return log_entries.first().action_time
        return None
    mostrar_data_change.short_description = 'Última Alteração'


class ListingMaintenance(admin.ModelAdmin):
    list_display = ('id', 'ativo__nome', 'operador', 'chamado_top_desk', 'chamado_externo', 'dias_atraso', 'status')
    list_display_links = ('id', 'ativo__nome',)
    search_fields = ('id', 'chamado_top_desk', 'ativo__nome__icontains',)
    list_filter = ('tipo_manutencao', 'status',)
    list_per_page = 20


class ListingAssetCart(admin.ModelAdmin):
    list_display = ('carrinho__usuario_sessao', 'ativo__nome')
    list_display_links = ('carrinho__usuario_sessao',)
    search_fields = ('ativo__nome__icontains',)
    list_per_page = 20
    actions = ['delete_selected']


class ListingAsset(admin.ModelAdmin):
    list_display = ('id', 'nome', 'patrimonio', 'numero_serie')
    search_fields = ('id', 'nome', 'patrimonio', 'numero_serie', 'operador__nome__icontains', 'modelo__nome__icontains',)
    list_filter = ('modelo', 'tipo')
    list_per_page = 20


class ListingMovement(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'usuario', 'status')
    search_fields = ('id', 'tipo', 'usuario__username__icontains',)
    list_filter = ('tipo', 'status',)
    list_per_page = 20


class ListingMovementAsset(admin.ModelAdmin):
    list_display = ('ativo__nome', 'movimento__id', 'devolvido')
    search_fields = ('ativo__nome__icontains', 'movimento__id',)
    list_filter = ('devolvido',)
    list_per_page = 20


class ListingMovementAccessory(admin.ModelAdmin):
    list_display = ('acessorio__nome', 'movimento__id',
                    'quantidade', 'quantidade_devolvida')
    search_fields = ('movimento__id', 'acessorio__nome')
    list_per_page = 20

class ListingConteudoTermo(admin.ModelAdmin):
    list_display = ('versao', 'tipo','data_criacao')
    search_fields = ('versao', 'tipo')
    list_filter = ('tipo',)
    list_per_page = 20


# Novos registros e modificações

admin.site.unregister(User)
admin.site.register(User, ListingUsers)
admin.site.register(Maintenance, ListingMaintenance)
admin.site.register(Asset, ListingAsset)
admin.site.register(Movement, ListingMovement)
admin.site.register(MovementAsset, ListingMovementAsset)
admin.site.register(MovementAccessory, ListingMovementAccessory)
admin.site.register(AssetCart, ListingAssetCart)
admin.site.register(ConteudoTermo, ListingConteudoTermo)
