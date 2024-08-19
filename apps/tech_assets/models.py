from datetime import datetime
from typing import Iterable
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from django.forms import ValidationError


class Manufacturer(models.Model):
    nome = models.CharField(max_length=100, null=False, unique=True)
    telefone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Fabricante'
        verbose_name_plural = 'Fabricantes'

    def __str__(self) -> str:
        return self.nome


class CostCenter(models.Model):
    nome = models.CharField(max_length=100, null=False)
    responsavel = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(null=False, unique=True)

    class Meta:
        verbose_name = 'Centro de Custo'
        verbose_name_plural = 'Centros de Custo'

    def __str__(self) -> str:
        return self.numero


class AssetType(models.Model):

    nome = models.CharField(max_length=100, null=False, unique=True)
    descricao = models.TextField(max_length=400, null=True, blank=True)

    class Meta:
        verbose_name = 'Tipo de Ativo'
        verbose_name_plural = 'Tipos de Ativo'

    def __str__(self) -> str:
        return self.nome


class AssetModel(models.Model):
    tipo = models.ForeignKey(
        AssetType, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100, null=False, blank=False)
    fabricante = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, null=True, blank=True)
    descricao = models.TextField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.nome


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
        ('separado', 'Separado'),
    ]

    nome = models.CharField(max_length=100, null=True, blank=True, unique=True)
    patrimonio = models.CharField(
        max_length=100, null=True, blank=True, unique=True)
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
        AssetModel, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Ativo'
        verbose_name_plural = 'Ativos'

    def __str__(self):
        return self.nome


class AssetInfo(models.Model):
    ativo = models.ForeignKey(Asset, on_delete=models.CASCADE)
    fabricante = models.ForeignKey(
        Manufacturer, on_delete=models.SET_NULL, null=True, blank=True)
    memoria = models.CharField(max_length=100, null=True, blank=True)
    armazenamento = models.CharField(max_length=100, null=True, blank=True)
    processador = models.CharField(max_length=100, null=True, blank=True)
    so = models.CharField(max_length=100, null=True, blank=True)
    versao_so = models.CharField(max_length=100, null=True, blank=True)
    licenca_so = models.CharField(max_length=100, null=True, blank=True)
    data_instalacao_so = models.DateField(null=True, blank=True, default='')
    data_garantia = models.DateField(null=True, blank=True, default='')
    endereco_mac = models.CharField(max_length=40, null=True, blank=True)
    ultimo_logon = models.DateField(null=True, blank=True, default='')
    ultimo_scan = models.DateField(null=True, blank=True, default='')

    def __str__(self):
        return f'{self.ativo.nome}'


class Movement(models.Model):
    STATUS_CHOICES = [
        ('pendente_aprovação', 'Aprovação Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('atrasado', 'Atrasado'),
    ]

    TIPOS = [
        ('transferencia', 'Transferência'),
        ('emprestimo', 'Empréstimo'),
        ('baixa', 'Baixa')
    ]

    ativos = models.ManyToManyField(Asset, through='MovementAsset')
    tipo = models.CharField(
        max_length=50, choices=TIPOS, default='emprestimo')
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='allocated_asset')
    centro_de_custo = models.ForeignKey(
        CostCenter, on_delete=models.CASCADE, related_name='allocated_asset')
    data_movimento = models.DateTimeField(default=datetime.now)
    data_devolucao_prevista = models.DateTimeField(null=True, blank=True)
    data_devolucao_real = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pendente_aprovação')
    chamado_top_desk = models.CharField(
        max_length=100, null=False, default=None)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Movimento Tipo: {self.tipo} ID: {self.id} para o usuário {self.usuario} no centro de custo {self.centro_de_custo}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Verifica se é uma nova instância
        ativos = kwargs.pop('ativos', None)
        aprovador = kwargs.pop('aprovador', None)
        super(Movement, self).save(*args, **kwargs)

        if is_new:
            print(f'DEBUG :: DENTRO DO SAVE DO MOVEMENT :: IS NEW!')
            if ativos:
                print(f'DEBUG :: DENTRO DO SAVE DO MOVEMENT :: EXISTEM OS ATIVOS!')
                for ativo in ativos:
                    MovementAsset.objects.create(ativo=ativo, movimento=self)  
                print(f'DEBUG :: DENTRO DO SAVE DO MOVEMENT :: CRIOU OS MOVEMENT ASSETS!')
            # Cria uma nova aprovação automaticamente
            print(f'DEBUG :: DENTRO DO SAVE DO MOVEMENT :: CHAMANDO A CRIACAO DE APPROVAL!')
            Approval.objects.create(movimentacao=self, aprovador=aprovador)

    def esta_atrasado(self):
        if self.status == 'em_andamento' and datetime.now() > self.data_devolucao_prevista:
            return True
        return False

    def marcar_como_concluido(self):
        self.status = 'concluido'
        self.data_devolucao_real = datetime.now()
        self.save()

    def dias_de_atraso(self):
        if self.status == 'em_andamento' and self.esta_atrasado():
            return (datetime.now() - self.data_devolucao_prevista).days
        return 0

    class Meta:
        ordering = ['-data_movimento']
        verbose_name = 'Alocação de Ativo'


class MovementAsset(models.Model):
    ativo = models.ForeignKey(Asset,  on_delete=models.CASCADE)
    movimento = models.ForeignKey(Movement, on_delete=models.CASCADE)
    return_condition = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.id


class Cart(models.Model):
    # ativos = models.ManyToManyField(Asset, through='AssetCart')
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

    MAINTENANCE_TYPES = [
        ('interna', 'Interna'),
        ('externa', 'Externa'),
    ]

    tipo_manutencao = models.CharField(
        max_length=100, choices=MAINTENANCE_TYPES, default='interna')
    ativo = models.ForeignKey(Asset, on_delete=models.CASCADE)
    operador = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='operator')
    data_inicio = models.DateField()
    data_prevista_fim = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    chamado_top_desk = models.CharField(
        max_length=100, null=False, blank=False)
    chamado_externo = models.CharField(
        max_length=100, null=True, blank=True)
    descricao = models.TextField()
    custo = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.BooleanField(default=True, null=False, blank=False)
    dias_atraso = models.IntegerField(default=0)

    def conclusao_atrasada(self):
        if self.data_prevista_fim:
            if self.status:
                if isinstance(self.data_prevista_fim, datetime):
                    data_prevista_fim = self.data_prevista_fim
                else:
                    data_prevista_fim = datetime.combine(
                        self.data_prevista_fim, datetime.min.time())

                if datetime.now() > data_prevista_fim:
                    return True
        return False

    def marcar_como_finalizada(self):
        self.status = False
        self.data_fim = datetime.now()
        self.save()

    def dias_de_atraso(self):
        if self.data_prevista_fim:
            if self.status and self.conclusao_atrasada():
                if isinstance(self.data_prevista_fim, datetime):
                    data_prevista_fim = self.data_prevista_fim
                else:
                    data_prevista_fim = datetime.combine(
                        self.data_prevista_fim, datetime.min.time())
                self.dias_atraso = (datetime.now() - data_prevista_fim).days
                self.save()

    class Meta:
        ordering = ['-data_inicio']
        verbose_name = 'Manutenção'

    def __str__(self):
        return f'Manutenção: {self.id}'


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
    movimentacao = models.ForeignKey(
        Movement, on_delete=models.CASCADE, related_name='approver')
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_modificacao = models.DateTimeField(auto_now=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.id}'
        # return f'Apovação criada para analise do aprovador {self.aprovador.username}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Verifica se é uma nova instância
        super(Approval, self).save(*args, **kwargs)

        if is_new:
            print(f'DEBUG :: DENTRO DO SAVE DO APPROVAL :: IS NEW!')
            print(f'DEBUG :: DENTRO DO SAVE DO APPROVAL :: CHAMANDO MUDAR STATUS ATIVO!')
            self.mudar_status_ativo('separado')


    def aprovar_movimentacao(self):
        self.status = 'aprovado'
        self.data_conclusao = datetime.now()
        self.mudar_status_ativo('separado')
        self.save()

    def reprovar_movimentacao(self):
        self.status = 'reprovado'
        self.data_conclusao = datetime.now()
        self.mudar_status_ativo('em_estoque')
        self.save()

    def mudar_status_ativo(self, status):
        print(f'DEBUG :: DENTRO DO MUDAR STATUS ATIVO! STATUS PASSADO {status}')
        # Muda status do ativo de separado para pendente_aprovacao
        if MovementAsset.objects.filter(movimento=self.movimentacao).exists():
            print(f'DEBUG :: MUDAR STATUS ATIVO :: ACHOU MOVEMENT ASSET!')
            ativos_id = [ativo.ativo_id for ativo in MovementAsset.objects.filter(
                movimento=self.movimentacao)]

        if ativos_id:
            print(f'DEBUG :: MUDAR STATUS ATIVO :: EXISTEM ASSETS!')
            ativos = Asset.objects.filter(id__in=ativos_id)

        for ativo in ativos:
            print(f'DEBUG :: MUDAR STATUS ATIVO :: DENTRO DO FOR!')
            if Maintenance.objects.filter(ativo=ativo).exists():
                print(f'DEBUG :: MUDAR STATUS ATIVO :: DENTRO DO IF FILTRA ASSET :: "TEM MANUTENCAO"!')
                ativo.status = 'em_manutencao'
                ativo.save()
            
            else:
                print(f'DEBUG :: MUDAR STATUS ATIVO :: DENTRO DO IF FILTRA ASSET :: "NÃO EXISTE MANUTENCAO"!')
                ativo.status = status
                ativo.save()
