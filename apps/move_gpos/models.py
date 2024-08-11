from django.db import models
from django.contrib.auth.models import User

# Create your models here.

"""
class GPOS(models.Model):

    id_gpos_mtvd_bd = models.IntegerField(null=False, blank=False)
    pos_number = models.IntegerField(null=False, blank=False)
    primary = models.BooleanField(default=True)
    mac_address = models.CharField(max_length=50)
    description = models.TextField(null=True)
    loja = models.CharField(null=False, max_length=100)
    pdv = models.CharField(null=False, max_length=100)
    active = models.BooleanField(default=False)

    # Usuário que cadastrou GPOS
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        blank=False,
        related_name='gpos'
    )

    # Data de inclusão
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Data de inclusão
    ultima_modificacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return

    def __unicode__(self):
        return


class Request(models.Model):

    gpos = models.ForeignKey(GPOS, on_delete=models.SET_NULL, null=True,
                             editable=False, blank=False, related_name='request')
    pdv_atual = models.CharField(null=False, max_length=100)
    loja_atual = models.CharField(null=False, max_length=100)
    novo_pdv = models.CharField(null=False, max_length=100)
    fila = models.BooleanField(default=False)
    concluida = models.BooleanField(default=False)

    # Usuário que cadastrou requisição
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        blank=False,
        related_name="user"
    )

    # Data de inclusão
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Data de inclusão
    ultima_modificacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return

    def __unicode__(self):
        return
"""