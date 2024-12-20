from datetime import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


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
    numero = models.CharField(null=True, blank=True)

    class Meta:
        verbose_name = 'Centro de Custo'
        verbose_name_plural = 'Centros de Custo'

    def __str__(self) -> str:
        return self.nome


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
    nome = models.CharField(max_length=100, null=False,
                            blank=False, unique=True)
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
        if self.local_pai:
            return f'{self.nome} ({self.local_pai.nome})'
        return self.nome

    def __unicode__(self):
        return

    class Meta:
        verbose_name = 'Localização'
        verbose_name_plural = 'Localizações'


class Accessory(models.Model):

    TIPO_CHOICES = [
        ('perifericos', 'Periférico(s) (E/S)'),
        ('mochilas', 'Mochila(s)'),
        ('carregadores', 'Carregador(es)'),
        ('cabos', 'Cabo(s)'),
        ('outros', 'Outro(s)')
    ]

    nome = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(
        max_length=50, choices=TIPO_CHOICES, blank=False, null=False)
    fabricante = models.ForeignKey(
        Manufacturer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.tipo} - {self.nome} | {self.modelo} | {self.fabricante}'


class Asset(models.Model):
    STATUS_CHOICES = [
        ('em_uso', 'Em Uso'),
        ('transferido', 'Transferido'),
        ('em_manutencao', 'Em Manutenção'),
        ('em_estoque', 'Em Estoque'),
        ('baixado', 'Baixado'),
        ('separado', 'Separado'),
        ('nao_devolvido', 'Não Devolvido')
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
    mongo_id = models.CharField(max_length=100, unique=True, null=True)

    class Meta:
        verbose_name = 'Ativo'
        verbose_name_plural = 'Ativos'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Asset, self).save(*args, **kwargs)

        #if is_new:
        #    AssetInfo.objects.get_or_create(ativo=self)

'''
class AssetInfo(models.Model):
    ativo = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name='assetinfo')
    fabricante = models.ForeignKey(
        Manufacturer, on_delete=models.SET_NULL, null=True, blank=True)
    memoria = models.CharField(max_length=100, null=True, blank=True)
    armazenamento = models.CharField(max_length=100, null=True, blank=True)
    processador = models.CharField(max_length=100, null=True, blank=True)
    plataforma = models.CharField(max_length=100, null=True, blank=True)
    versao_plataforma = models.CharField(max_length=100, null=True, blank=True)
    licenca_plataforma = models.CharField(
        max_length=100, null=True, blank=True)
    data_instalacao_plataforma = models.DateField(null=True, blank=True)
    data_garantia = models.DateField(null=True, blank=True)
    endereco_mac = models.CharField(max_length=40, null=True, blank=True)
    ultimo_logon = models.DateTimeField(null=True, blank=True)
    ultimo_scan = models.DateTimeField(null=True, blank=True)
    data_registro = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.ativo.nome}'
'''

class LogonInAsset(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='logon_user')
    user_name = models.CharField(max_length=100, null=True, blank=True)
    ativo = models.ForeignKey(
        Asset, on_delete=models.SET_NULL, null=True, related_name='logon_asset')
    data_logon = models.DateTimeField(null=True, blank=True)


class Movement(models.Model):
    STATUS_CHOICES = [
        ('pendente_aprovacao', 'Aprovação Pendente'),
        ('pendente_entrega', 'Pendente Entrega'),
        ('em_devolucao', 'Devolução em Andamento'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('atrasado', 'Atrasado'),
    ]

    TIPOS = [
        ('transferencia', 'Transferência'),
        ('emprestimo', 'Empréstimo'),
        ('baixa', 'Baixa')
    ]

    ativos = models.ManyToManyField(Asset, blank=True, through='MovementAsset')
    acessorios = models.ManyToManyField(
        Accessory, blank=True, through='MovementAccessory')
    tipo = models.CharField(
        max_length=50, choices=TIPOS, default='emprestimo')
    usuario_cedente = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_send')
    centro_de_custo_cedente = models.ForeignKey(
        CostCenter, on_delete=models.CASCADE, related_name='cc_send')
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_recept')
    centro_de_custo_recebedor = models.ForeignKey(
        CostCenter, on_delete=models.CASCADE, related_name='cc_recept')
    data_movimento = models.DateTimeField(auto_now_add=False)
    data_devolucao_prevista = models.DateTimeField(null=True, blank=True)
    data_devolucao_real = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pendente_aprovacao')
    chamado_top_desk = models.CharField(
        max_length=100, null=False, default=None)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Movimento Tipo: {self.tipo} ID: {self.id} para o usuário {self.usuario} no centro de custo {self.centro_de_custo_recebedor}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        ativos = kwargs.pop('ativos', None)
        aprovador = kwargs.pop('aprovador', None)
        acessorios = kwargs.pop('acessorios', None)
        super(Movement, self).save(*args, **kwargs)

        if is_new:
            if ativos:
                for ativo in ativos:
                    MovementAsset.objects.create(ativo=ativo, movimento=self)

            if acessorios:  # Verifica se foi passado alguma lista de acessórios no form da movimentação
                # Se entrar aqui irá criar e salvar as instâncias de MovementAccessory
                # Onde tera a relação de acessório e movimento com valor de quantidade
                for acessorio_id, total_quantidade in acessorios.items():
                    try:
                        acessorio = Accessory.objects.get(id=acessorio_id)
                        MovementAccessory.objects.create(
                            movimento=self,
                            acessorio=acessorio,
                            quantidade=total_quantidade
                        )
                    except Accessory.DoesNotExist as error:
                        print(f'ERROR :: {error}')

            Approval.objects.create(movimentacao=self, aprovador=aprovador)

    def esta_atrasado(self):
        if self.status == 'em_andamento' and timezone.now() > self.data_devolucao_prevista:
            return True
        return False

    def marcar_como_concluido(self):
        self.status = 'concluido'
        self.data_devolucao_real = timezone.now()
        self.save()

    def dias_de_atraso(self):
        if self.status == 'em_andamento' and self.esta_atrasado():
            return (timezone.now() - self.data_devolucao_prevista).days
        return 0

    class Meta:
        ordering = ['-data_movimento']
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'


class MovementAsset(models.Model):
    ativo = models.ForeignKey(Asset,  on_delete=models.CASCADE)
    movimento = models.ForeignKey(Movement, on_delete=models.CASCADE)
    devolvido = models.BooleanField(default=False)
    return_condition = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.ativo.nome)

    class Meta:
        verbose_name = 'Movimentação / Ativo'
        verbose_name_plural = 'Movimentações / Ativo'

    def marcar_como_devolvido(self):
        print(f'DEVOLVENDO :: ASSET {self.ativo.nome}')
        self.devolvido = True
        ativo = get_object_or_404(Asset, pk=self.ativo.id)
        if ativo:
            if Maintenance.objects.filter(ativo=ativo, status=True).exists():
                ativo.status = 'em_manutencao'
                ativo.save()
            else:
                ativo.status = 'em_estoque'
                ativo.save()
        self.save()


class MovementAccessory(models.Model):
    acessorio = models.ForeignKey(Accessory,  on_delete=models.CASCADE)
    movimento = models.ForeignKey(Movement, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    quantidade_devolvida = models.PositiveIntegerField(
        null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.quantidade} x {self.acessorio.nome}"

    class Meta:
        verbose_name = 'Movimentação / Acessório'
        verbose_name_plural = 'Movimentações / Acessório'

    def soma_quantidade_devolvida(self, quantidade):
        if not self.quantidade_devolvida + quantidade > self.quantidade:
            self.quantidade_devolvida += quantidade
            self.save()


class Cart(models.Model):
    usuario_sessao = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='session_user_cart')
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class AssetCart(models.Model):
    ativo = models.OneToOneField(Asset,  on_delete=models.CASCADE)
    carrinho = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Ativo / Carrinho'
        verbose_name_plural = 'Ativos / Carrinho'


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
        verbose_name_plural = 'Manutenções'

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
        return str(self.id)


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
        return str(self.id)
        # return f'Apovação criada para analise do aprovador {self.aprovador.username}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Approval, self).save(*args, **kwargs)

        if is_new:
            self.mudar_status_ativos('separado')

    def aprovar_movimentacao(self):
        self.status_aprovacao = 'aprovado'
        self.data_conclusao = datetime.now()
        # self.mudar_status_ativos('separado')
        self.mudar_status_movimentacao('aprovar')
        self.save()

        termo = Termo.objects.create(
            movimentacao=self.movimentacao, aprovacao=self)
        termo.save()

    def reprovar_movimentacao(self):
        self.status_aprovacao = 'reprovado'
        self.data_conclusao = datetime.now()
        self.mudar_status_ativos('em_estoque')

        for movement_accessory in MovementAccessory.objects.filter(movimento=self.movimentacao):
            movement_accessory.soma_quantidade_devolvida(
                movement_accessory.quantidade)

        self.mudar_status_movimentacao('reprovar')
        self.save()

    def mudar_status_ativos(self, status, *args, **kwargs):
        origin_model_term = kwargs.pop('origin_model_term', False)

        # Muda status do ativo de separado para pendente_aprovacao
        if MovementAsset.objects.filter(movimento=self.movimentacao).exists():
            ativos_id = [ativo.ativo_id for ativo in MovementAsset.objects.filter(
                movimento=self.movimentacao)]

            if ativos_id:
                ativos = Asset.objects.filter(id__in=ativos_id)

            for ativo in ativos:
                if Maintenance.objects.filter(ativo=ativo, status=True).exists():
                    ativo.status = 'em_manutencao'
                    ativo.save()
                elif Movement.objects.filter(ativos=ativo, tipo='transferencia').exists() and origin_model_term:
                    ativo.status = 'transferido'
                    ativo.save()
                elif Movement.objects.filter(ativos=ativo, tipo='baixa').exists() and origin_model_term:
                    ativo.status = 'baixado'
                    ativo.save()
                else:
                    ativo.status = status
                    ativo.save()
                    if status == 'em_estoque':
                        movementAsset = MovementAsset.objects.get(
                            ativo=ativo.id, movimento=self.movimentacao.id)
                        movementAsset.marcar_como_devolvido()

    def mudar_status_movimentacao(self, status):

        movimento = self.movimentacao

        if movimento:
            if status == 'aprovar':
                movimento.status = 'pendente_entrega'
            elif status == 'reprovar':
                for item in MovementAsset.objects.filter(movimento=movimento):
                    item.devolvido = True
                    item.save()
                movimento.status = 'concluido'
                movimento.data_devolucao_real = timezone.now()
            movimento.save()


class ConteudoTermo(models.Model):
    versao = models.CharField(max_length=12, unique=True, editable=False)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(
        max_length=100, choices=Movement.TIPOS, default='emprestimo')
    publicar = models.BooleanField(default=False)

    def __str__(self):
        return f"Termo Versão {self.versao}"

    def save(self, *args, **kwargs):
        if not self.versao:
            hoje = datetime.now().strftime('%Y.%m.%d')
            contador_hoje = ConteudoTermo.objects.filter(
                versao__startswith=hoje).count() + 1
            self.versao = f"{hoje}.{contador_hoje}"

        super().save(*args, **kwargs)

        if self.publicar:
            termos = Termo.objects.select_related('movimentacao').filter(
                    movimentacao__status__in=[
                        'em_andamento', 'atrasado', 'pendente_aprovacao', 'pendente_entrega'],
                    movimentacao__tipo=self.tipo
                )

            termos.update(
                        aceite_usuario='pendente_aceite_novos_termos',
                        status_resposta=False
                    )
            
            for termo in termos:
                termo.conteudo_termo = self
                print(f'DEBUG :: VALOR AGORA DO TERMO {termo.id} :: {termo.conteudo_termo} ')
                termo.save()


def get_latest_termo_version():
    return ConteudoTermo.objects.order_by('-data_criacao').first()


class Termo(models.Model):

    status_aceite = [
        ('aceito', 'Aceito'),
        ('pendente', 'Pendente'),
        ('recusado', 'Recusado'),
        ('pendente_aceite_novos_termos', 'Pendente Aceitação de Novos Termos')
    ]

    movimentacao = models.ForeignKey(
        Movement, on_delete=models.CASCADE, related_name='termo_movimentacao')
    aprovacao = models.ForeignKey(
        Approval, on_delete=models.CASCADE, related_name='approval')
    conteudo_termo = models.ForeignKey(
        ConteudoTermo, on_delete=models.PROTECT, related_name='termos', default=get_latest_termo_version
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_resposta = models.DateTimeField(null=True, blank=True)
    status_resposta = models.BooleanField(default=False)
    aceite_usuario = models.CharField(
        max_length=100, choices=status_aceite, default='pendente')
    justificativa = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            conteudo_termo = ConteudoTermo.objects.filter(
                tipo=self.movimentacao.tipo).latest('versao')
            if conteudo_termo:
                self.conteudo_termo = conteudo_termo
        super().save(*args, **kwargs)

    def marcar_como_aceito(self, movimentacao):
        self.status_resposta = True
        self.data_resposta = timezone.now()
        self.aceite_usuario = 'aceito'
        if movimentacao.tipo == 'emprestimo':
            movimentacao.status = 'em_andamento'
        elif movimentacao.tipo in ['transferencia', 'baixa']:
            movimentacao.status = 'concluido'

        movimentacao.save()
        self.aprovacao.mudar_status_ativos('em_uso', origin_model_term=True)
        self.save()

    def marcar_como_recusa(self, movimentacao):
        self.status_resposta = True
        self.data_resposta = timezone.now()
        self.aceite_usuario = 'recusado'
        movimentacao.status = 'concluido'
        movimentacao.data_devolucao_real = timezone.now()
        movimentacao.save()
        self.aprovacao.mudar_status_ativos('em_estoque')
        self.aprovacao.mudar_status_movimentacao('reprovar')
        for movement_accessory in MovementAccessory.objects.filter(movimento=movimentacao):

            movement_accessory.soma_quantidade_devolvida(
                movement_accessory.quantidade)

        self.save()


class ReturnTerm(models.Model):
    movimentacao = models.ForeignKey(
        Movement, on_delete=models.CASCADE, related_name='returned')
    usuario_recebedor = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='user_recept_return')
    data_retorno = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    observacao = models.TextField(max_length=400, blank=True, null=True)

    def save(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        self.movimentacao.marcar_como_concluido()
        if usuario:
            self.usuario_recebedor = usuario
        super(ReturnTerm, self).save(*args, **kwargs)
        if self._state.adding:
            super(ReturnTerm, self).save(*args, **kwargs)
