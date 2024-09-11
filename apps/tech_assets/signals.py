from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver


@receiver(post_migrate)
def cria_grupos_iniciais(sender, **kwargs):
    grupos = ['Administradores', 'Aprovadores TI', 'Suporte', 'TH', 'Basico', 'Move GPOS']
    
    for grupo in grupos:
        Group.objects.get_or_create(name=grupo)