import django_filters

from apps.tech_assets.models import *
from django.db.models import Count


class AssetFilter(django_filters.FilterSet):

    nome = django_filters.CharFilter(label='Nome', lookup_expr='icontains')
    patrimonio = django_filters.CharFilter(
        label='Patrimônio', lookup_expr='icontains')
    tipo__nome = django_filters.ModelChoiceFilter(
        label='Tipo Ativo', field_name='tipo', lookup_expr='exact', queryset=AssetModel.objects.all())
    modelo__nome = django_filters.ModelChoiceFilter(
        label='Modelo Ativo', field_name='modelo', lookup_expr='exact', queryset=AssetModel.objects.all())
    numero_serie = django_filters.CharFilter(
        label='Número de Série', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(
        choices=Asset.STATUS_CHOICES,
        label="Status"
    )


    class Meta:
        model = Asset
        fields = {
            'nome', 'patrimonio', 'tipo', 'modelo', 'numero_serie', 'status',
        }


class AccessoryFilter(django_filters.FilterSet):

    nome = django_filters.CharFilter(label='Nome', lookup_expr='icontains')
    tipo = django_filters.ChoiceFilter(
        choices=Accessory.TIPO_CHOICES,
        label="Tipo de Acessório",
    )
    modelo = django_filters.CharFilter(label='Modelo', lookup_expr='icontains')
    fabricante = django_filters.ModelChoiceFilter(label='Fabricante', queryset=Manufacturer.objects.all())


    class Meta:
        model = Accessory
        fields = {
            'nome', 'tipo', 'modelo', 'fabricante'
        }


class CostCenterFilter(django_filters.FilterSet):

    nome = django_filters.CharFilter(label='Nome', lookup_expr='icontains')
    responsavel = django_filters.CharFilter(label='Responsável', lookup_expr='icontains')
    numero = django_filters.CharFilter(label='Número do Centro de Custo', lookup_expr='icontains')


    class Meta:
        model = CostCenter
        fields = {
            'nome', 'responsavel', 'numero'
        }

class ManufacturerFilter(django_filters.FilterSet):

    nome = django_filters.CharFilter(label='Nome', lookup_expr='icontains')


    class Meta:
        model = Manufacturer
        fields = {
            'nome',
        }

class LocationFilter(django_filters.FilterSet):

    nome = django_filters.CharFilter(label='Nome', lookup_expr='icontains')
    local_pai = django_filters.ModelChoiceFilter(label='Local Pai', queryset=Location.objects.annotate(num_sub_locations=Count('sub_locations')).filter(num_sub_locations__gt=0))

    class Meta:
        model = Location
        fields = {
            'nome', 'local_pai'
        }

class AssetModelFilter(django_filters.FilterSet):

    nome = django_filters.CharFilter(label='Nome', lookup_expr='icontains')
    tipo = django_filters.ModelChoiceFilter(label='Tipo', queryset=AssetType.objects.all())
    fabricante = django_filters.ModelChoiceFilter(label='Fabricante', queryset=Manufacturer.objects.all())

    class Meta:
        model = AssetModel
        fields = {
            'nome', 'tipo', 'fabricante'
        }

class AssetTypeFilter(django_filters.FilterSet):

    nome = django_filters.CharFilter(label='Nome', lookup_expr='icontains')


    class Meta:
        model = AssetType
        fields = {
            'nome',
        }

class TermoFilter(django_filters.FilterSet):

    responsavel = django_filters.CharFilter(label='Nome Responsável', field_name='movimentacao__usuario__first_name', lookup_expr='icontains')
    matricula = django_filters.CharFilter(label='Matricula Responsável', field_name='movimentacao__usuario__user_employee__employee__matricula', lookup_expr='exact')
    numero = django_filters.NumberFilter(label='Número da Movimentação', field_name='movimentacao__id', lookup_expr='exact')
    aceite_usuario = django_filters.ChoiceFilter(
        choices=Termo.status_aceite,
        label="Status",
    )
    chamado = django_filters.CharFilter(label='Chamado Relacionado', field_name='movimentacao__chamado_top_desk', lookup_expr='icontains')
    centro_custo = django_filters.CharFilter(label='Centro de Custo Recebedor', field_name='movimentacao__centro_de_custo_recebedor__nome', lookup_expr='icontains')
    ativo = django_filters.CharFilter(label='Ativo Relacionado', field_name='movimentacao__ativos__nome', lookup_expr='icontains')
    tipo = django_filters.ChoiceFilter(
        field_name = 'movimentacao__tipo',
        choices=Movement.TIPOS,
        label='Tipo de Movimenação',
    )
    status_movimento = django_filters.ChoiceFilter(
        field_name = 'movimentacao__status',
        choices=Movement.STATUS_CHOICES,
        label='Status da Movimenação',
    )


    class Meta:
        model = Termo
        fields = {
            'aceite_usuario',
        }

class ApprovalFilter(django_filters.FilterSet):

    responsavel = django_filters.CharFilter(label='Nome Responsável', field_name='movimentacao__usuario__first_name', lookup_expr='icontains')
    matricula = django_filters.CharFilter(label='Matricula Responsável', field_name='movimentacao__usuario__user_employee__employee__matricula', lookup_expr='exact')
    numero = django_filters.NumberFilter(label='Número da Movimentação', field_name='movimentacao__id', lookup_expr='exact')
    status_aprovacao = django_filters.ChoiceFilter(
        choices=Approval.STATUS_APPROVAL,
        label="Status",
    )
    chamado = django_filters.CharFilter(label='Chamado Relacionado', field_name='movimentacao__chamado_top_desk', lookup_expr='icontains')
    centro_custo = django_filters.CharFilter(label='Centro de Custo Recebedor', field_name='movimentacao__centro_de_custo_recebedor__nome', lookup_expr='icontains')
    ativo = django_filters.CharFilter(label='Ativo Relacionado', field_name='movimentacao__ativos__nome', lookup_expr='icontains')
    tipo = django_filters.ChoiceFilter(
        field_name = 'movimentacao__tipo',
        choices=Movement.TIPOS,
        label='Tipo de Movimenação',
    )


    class Meta:
        model = Approval
        fields = {
            'status_aprovacao',
        }