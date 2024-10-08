from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group
from apps.tech_persons.models import *
from django.contrib.admin.models import ADDITION, CHANGE, LogEntry


class ListingEmployee(admin.ModelAdmin):
    list_display = ('id', 'nome', 'matricula')
    list_display_links = ('id', 'nome')
    search_fields = ('id', 'nome', 'matricula')
    list_per_page = 10

class UserEmployeeInline(admin.StackedInline):
    model = UserEmployee
    can_delete = False
    verbose_name_plural = 'User Employee'
    fk_name = 'user'

    
class ListandoUsers(UserAdmin):
    list_display = ("id", "username", "email", "is_staff", "mostrar_grupo",
                    "is_superuser", "mostrar_data_add", "mostrar_data_change",)
    list_display_links = ("id", "username")
    inlines = (UserEmployeeInline,)
    
    # Campos somente de leitura
    readonly_fields = ('date_joined', 'last_login')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(ListandoUsers, self).get_inline_instances(request, obj)

    def mostrar_grupo(self, user):
        obj = Group.objects.filter(user=user.id)
        if obj:
            grupos = ", ".join([x.name for x in obj][0:2])
            if len([x.name for x in obj]) > 3:
                return grupos + ", ..."
            else:
                return grupos
        else:
            return "-"
    mostrar_grupo.short_description = "Grupos"

    
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

# Registro dos forms
admin.site.unregister(User)
admin.site.register(User, ListandoUsers)
admin.site.register(Employee, ListingEmployee)