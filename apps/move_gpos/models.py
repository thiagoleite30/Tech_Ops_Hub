from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.utils import timezone

from apps.tech_assets.models import Asset, Location

class GPOS(models.Model):
    # Campos do modelo
    id = models.IntegerField(primary_key=True, verbose_name="ID GPOS")
    ativo = models.ForeignKey(Asset, on_delete=models.CASCADE)
    loja = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='loja_gpos', verbose_name="Loja")
    pdv = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pdv_gpos', verbose_name="PDV")
    description = models.TextField(verbose_name="Descrição", blank=True, null=True)
    active = models.BooleanField(default=True, db_index=True, verbose_name="Ativo")
    pos_number = models.IntegerField(verbose_name="Número do POS")
    only_pre_sales = models.BooleanField(default=False, verbose_name="Apenas Pré-Vendas")
    primary_pdv = models.BooleanField(default=False, verbose_name="PDV Primário")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    creator_user = models.CharField(max_length=100, verbose_name="Usuário Criador")
    last_update_date = models.DateTimeField(auto_now=True, null=True, verbose_name="Última Atualização MV")
    username_last_user_logon = models.CharField(max_length=100, null=True, verbose_name="Último usuário a fazer logon")
    code_last_user_logon = models.CharField(max_length=100, null=True, verbose_name="Código do último usuário a fazer logon")
    last_logon_date = models.DateTimeField(auto_now=False, null=True, db_index=True, verbose_name="Data último logon MV")
    computer_type = models.CharField(max_length=100, verbose_name="Tipo de Computador")
    blocked = models.BooleanField(default=False, db_index=True) # Define se o GPOS estará disponível para uma nova troca ou não
    is_mac = models.BooleanField(default=False, db_index=True) # Define se o GPOS é identificado com Mac ou IMEI
    
    class Meta:
        verbose_name = "GPOS"
        verbose_name_plural = "GPOSs"
        ordering = ['-creation_date']

    def __str__(self):
        return f'{self.pos_number}'
    
class Request(models.Model):
    
    gpos = models.ForeignKey(GPOS, on_delete=models.CASCADE)
    pdv_atual = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pdv_atual_request', verbose_name="PDV Atual") 
    loja_nova = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='loja_nova_request', verbose_name="Nova Loja")
    pdv_novo = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pdv_novo_request', verbose_name="Novo PDV")
    chamado = models.CharField(max_length=100, null=True, blank=True)
    existe_novo_pdv = models.BooleanField(default=False)
    concluida = models.BooleanField(default=False)
    data_inclusao = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(auto_now=False, null=True)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self)

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Verifica se é uma nova instância
        super(Request, self).save(*args, **kwargs)

        if is_new:
            gpos = GPOS.objects.get(pk=self.gpos.id)
            gpos.blocked = True
            gpos.save()