from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.utils import timezone

from apps.tech_assets.models import Asset, Location

class GPOS(models.Model):
    # Campos do modelo
    id = models.IntegerField(primary_key=True, verbose_name="ID GPOS")  # ID do GPOS
    ativo = models.ForeignKey(Asset, on_delete=models.CASCADE)
    loja = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='loja_gpos', verbose_name="Loja")  # Nome da Loja
    pdv = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pdv_gpos', verbose_name="PDV")  # Ponto de Venda
    description = models.TextField(verbose_name="Descrição", blank=True, null=True)  # Descrição do GPOS
    #mac_address = models.CharField(max_length=17, verbose_name="Endereço MAC")  # Endereço MAC do GPOS
    active = models.BooleanField(default=True, verbose_name="Ativo")  # Indica se o GPOS está ativo
    pos_number = models.IntegerField(verbose_name="Número do POS")  # Número do POS
    only_pre_sales = models.BooleanField(default=False, verbose_name="Apenas Pré-Vendas")  # Indica se o POS é apenas para pré-vendas
    primary_pdv = models.BooleanField(default=False, verbose_name="PDV Primário")  # Indica se é o PDV principal
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")  # Data de criação
    creator_user = models.CharField(max_length=255, verbose_name="Usuário Criador")  # Usuário que criou o registro
    last_update_date = models.DateTimeField(auto_now=False, null=True, verbose_name="Última Atualização MV")  # Última data de atualização
    computer_type = models.CharField(max_length=100, verbose_name="Tipo de Computador")  # Tipo de Computador
    blocked = models.BooleanField(default=False) # Define se o GPOS estará disponível para uma nova troca ou não
    is_mac = models.BooleanField(default=False) # Define se o GPOS é identificado com Mac ou IMEI
    
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
    data_conclusao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Verifica se é uma nova instância
        super(Request, self).save(*args, **kwargs)

        if is_new:
            gpos = GPOS.objects.get(pk=self.gpos.id)
            gpos.blocked = True
            gpos.save()
        else:
            if self.concluida:
                gpos = GPOS.objects.get(pk=self.gpos.id)
                gpos.blocked = False
                gpos.save()