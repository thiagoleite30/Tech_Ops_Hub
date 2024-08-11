from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from apps.tech_assets.models import Manufacturer

# Register your models here.
class ListingUsers(UserAdmin):
    list_display = ("id", "username", "email", "is_staff", "mostrar_grupo",
                    "is_superuser", "mostrar_data_add", "mostrar_data_change",)
    list_display_links = ("id", "username")
    
    # Aqui personaliza que na página de admin no formulário de usuário não pode ser alterada a informação de data de registo
    readonly_fields = ('date_joined', 'last_login')

    def mostrar_grupo(self, user):
        obj = Group.objects.filter(user=user.id)
        if obj:
            grupos = ", ".join([x.name for x in obj][0:2])
            # Por questão de adequação, vamos listar na tela inicial somente até 3 grupos, caso haja mais, concatena um ...
            if len([x.name for x in obj]) > 3:
                return grupos + ", ..."
            else:
                return grupos
        else:
            return "-"
    mostrar_grupo.short_description = "Grupos"

    """    def mostrar_data_add(self, obj):
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
    mostrar_data_add.short_description = "Data Inclusão"""
    
    def mostrar_data_add(self, obj):
        return User.objects.get(id=obj.id).date_joined
    # dando nome a coluna do list_display que irá mostrar essa informação
    mostrar_data_add.short_description = "Data Inclusão"

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
    mostrar_data_change.short_description = "Última Alteração"
    
class ListingManufacturer(admin.ModelAdmin):
    list_display = ("id", "nome")
    list_display_links = ("id", "nome")
    search_fields = ("id", "nome")
    list_per_page = 10
    
    
    # Register your models here.
# Remove o registro do UserAdmin padrão para que consigamos mostrar nosso personalizado
admin.site.unregister(User)
admin.site.register(User, ListingUsers)  # Registra o seu CustomUserAdmin
admin.site.register(Manufacturer, ListingManufacturer)