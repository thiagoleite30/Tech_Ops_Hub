from datetime import datetime
from typing import Iterable
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models


class Manufacturer(models.Model):
    nome = models.CharField(max_length=100, null=False, unique=True)
    telefone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    class Meta:
        verbose_name = 'Fabricante'
        verbose_name_plural = 'Fabricantes'

    def __str__(self) -> str:
        return self.nome


class CostCenter(models.Model):
    nome = models.CharField(max_length=100, null=False)
    responsavel = models.CharField(max_length=100, null=True)
    numero = models.CharField(null=False, unique=True)

    class Meta:
        verbose_name = 'Centro de Custo'
        verbose_name_plural = 'Centros de Custo'

    def __str__(self) -> str:
        return f'{self.nome} - {self.numero}'


'''
class User(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    departamento = models.ForeignKey(CostCenter, on_delete=models.CASCADE)
'''


class AssetType(models.Model):
    nome = models.CharField(max_length=100, null=False)
    descricao = models.TextField(max_length=400, null=True)

    class Meta:
        verbose_name = 'Tipo de Ativo'
        verbose_name_plural = 'Tipos de Ativo'

    def __str__(self) -> str:
        return self.nome


class AssetModel(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    fabricante = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, null=True, blank=True)
    descricao = models.TextField(max_length=400, null=True, blank=True)


class Location(models.Model):

    nome = models.CharField(max_length=100, unique=True, null=False)
    local_pai = models.ForeignKey('self', on_delete=models.SET_NULL,
                                  max_length=100, null=True, blank=True, related_name='sub_locations')

    def __str__(self):
        return self.nome

    def __unicode__(self):
        return

    class Meta:
        verbose_name = 'Localização'
        verbose_name_plural = 'Localizações'


class Asset(models.Model):
    STATUS_CHOICES = [
        ('em_uso', 'Em Uso'),
        ('em_manutencao', 'Em Manutenção'),
        ('em_estoque', 'Em Estoque'),
        ('descartado', 'Descartado'),
    ]

    SITE_CHOICES = [
        ('rio_quente', 'Rio Quente'),
        ('costa_do_sauipe', 'Costa do Sauipe'),
    ]

    nome = models.CharField(max_length=100, null=False)
    patrimonio = models.CharField(max_length=100, null=True, blank=True, unique=True)
    site = models.CharField(max_length=100, null=False,
                            choices=SITE_CHOICES, default='rio_quente')
    tipo = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True)
    numero_serie = models.CharField(max_length=100, unique=True, null=False)
    data_aquisicao = models.DateField(null=True, blank=True)
    valor_aquisicao = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, null=False, default='em_estoque')
    localizacao = models.ForeignKey(
        Location, on_delete=models.SET_NULL, max_length=100, blank=True, null=True)
    modelo = models.ForeignKey(
        Manufacturer, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Ativo'
        verbose_name_plural = 'Ativos'

    def __str__(self):
        return self.nome


class Loan(models.Model):
    STATUS_CHOICES = [
        ('pendente_aprovação', 'Aprovação Pendente'),
        ('emprestado', 'Emprestado'),
        ('devolvido', 'Devolvido'),
        ('atrasado', 'Atrasado'),
    ]

    ativos = models.ManyToManyField(Asset, through='LoanAsset')
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='allocated_asset')
    centro_de_custo = models.ForeignKey(
        CostCenter, on_delete=models.CASCADE, related_name='allocated_asset')
    data_emprestimo = models.DateTimeField(default=datetime.now)
    data_devolucao_prevista = models.DateTimeField(null=True, blank=True)
    data_devolucao_real = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pendente_aprovação')
    chamado_top_desk = models.CharField(
        max_length=100, null=False, default=None)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Empréstimo para o usuário {self.usuario.name} ({self.centro_de_custo.nome})'

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Verifica se é uma nova instância

        super(Loan, self).save(*args, **kwargs)

        if is_new:
            # Cria uma nova aprovação automaticamente
            Approval.objects.create(emprestimo=self)

    def esta_atrasado(self):
        if self.status == 'emprestado' and datetime.now() > self.data_devolucao_prevista:
            return True
        return False

    def marcar_como_devolvido(self):
        self.status = 'devolvido'
        self.data_devolucao_real = datetime.now()
        self.save()

    def dias_de_atraso(self):
        if self.status == 'emprestado' and self.esta_atrasado():
            return (datetime.now() - self.data_devolucao_prevista).days
        return 0

    class Meta:
        ordering = ['-data_emprestimo']
        verbose_name = 'Alocação de Ativo'


class LoanAsset(models.Model):
    ativo = models.OneToOneField(Asset,  on_delete=models.CASCADE)
    emprestimo = models.ForeignKey(Loan, on_delete=models.CASCADE)
    return_condition = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.id


class Cart(models.Model):
    ativos = models.ManyToManyField(Asset, through='AssetCart')
    usuario_sessao = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='session_user_cart')
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class AssetCart(models.Model):
    ativo = models.OneToOneField(Asset,  on_delete=models.CASCADE)
    carrinho = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Maintenance(models.Model):
    ativo = models.ForeignKey(Asset, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    descricao = models.TextField()
    custo = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Manutenção'
        
    def __str__(self):
        return self.id

class Software(models.Model):
    nome = models.CharField(max_length=100)
    versao = models.CharField(max_length=50)
    licenca = models.CharField(max_length=100)
    data_expiracao = models.DateField()


class NetworkDevice(models.Model):
    DEVICE_TYPES = [
        ('switch', 'Switch'),
        ('roteador', 'Roteador'),
        ('firewall', 'Firewall'),
    ]

    tipo = models.CharField(max_length=20, choices=DEVICE_TYPES)
    endereco_ip = models.GenericIPAddressField()
    mascara_rede = models.CharField(max_length=15)
    ativo = models.OneToOneField(Asset, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Dispositivo de Rede'
        verbose_name_plural = 'Dispositivos de Rede'
        
    def __str__(self):
        return self.id

class Approval(models.Model):
    STATUS_APPROVAL = [
        ('aprovado', 'Aprovado'),
        ('reprovado', 'Reprovado'),
        ('pendente', 'Pendente')
    ]

    aprovador = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='approver')
    status_aprovacao = models.CharField(
        max_length=20, choices=STATUS_APPROVAL, default='pendente')
    emprestimo_id = models.ForeignKey(
        Loan, on_delete=models.CASCADE, related_name='approver')
        
    def __str__(self):
        return f'Apovação criada para analise do aprovador {self.aprovador.username}'