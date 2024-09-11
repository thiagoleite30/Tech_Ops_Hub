from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.contrib.auth.models import User

from apps.tech_persons.models import Profile


@receiver(post_save, sender=User)
def cria_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()