import django_filters

from apps.tech_assets.models import Asset, AssetModel, AssetType

class AssetFilter(django_filters.FilterSet):
    STATUS_CHOICES = [
        ('em_uso', 'Em Uso'),
        ('transferido', 'Transferido'),
        ('em_manutencao', 'Em Manutenção'),
        ('em_estoque', 'Em Estoque'),
        ('baixado', 'Baixado'),
        ('separado', 'Separado'),
    ]

    nome = django_filters.CharFilter(label='Nome', lookup_expr='icontains')
    patrimonio = django_filters.CharFilter(label='Patrimônio', lookup_expr='icontains')
    tipo__nome = django_filters.ChoiceFilter(label='Tipo Ativo', field_name='tipo', lookup_expr='exact')
    modelo__nome = django_filters.ChoiceFilter(label='Modelo Ativo', field_name='modelo', lookup_expr='exact')
    numero_serie = django_filters.CharFilter(label='Número de Série', lookup_expr='icontains')
    #status = django_filters.ChoiceFilter(label='Status Ativo', field_name='status', lookup_expr='exact', choices= [ativo.status for ativo in Asset.objects.all().distinct('status')])
    status = django_filters.CharFilter(label='Status', lookup_expr='icontains')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['tipo__nome'].choices = [(tipo.nome, tipo.nome) for tipo in AssetType.objects.all()]
        self.filters['modelo__nome'].choices=[(modelo.nome, modelo.nome) for modelo in AssetModel.objects.all()]
    
    class Meta:
        model = Asset
        fields = {
            'nome', 'patrimonio', 'tipo', 'modelo', 'numero_serie', 'status',
        }