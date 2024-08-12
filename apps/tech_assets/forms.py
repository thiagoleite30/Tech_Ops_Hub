from django import forms
from apps.tech_assets.models import Asset, AssetModel, Loan, LoanAsset, Manufacturer, CostCenter, \
    AssetType, Location, Maintenance
from datetime import datetime


class ManufacturerForms(forms.ModelForm):
    form_name = 'Novo Fabricante'

    class Meta:
        model = Manufacturer
        exclude = []
        labels = {
            'nome': 'Nome',
            'email': 'E-mail',
            'telefone': 'Telefone',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Dell'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: fulano@dell.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: (XX) XXXXX-XXXX'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class CostCenterForms(forms.ModelForm):
    form_name = 'Novo Centro de Custo'

    class Meta:
        model = CostCenter
        exclude = []
        labels = {
            'nome': 'Nome',
            'responsavel': 'Responsável',
            'numero': 'Número do Centro de Custo',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Tecnologia da Informação'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Fulano De Tal'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '020103'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class AssetTypeForms(forms.ModelForm):
    form_name = 'Novo Tipo de Ativo'

    class Meta:
        model = AssetType
        exclude = []
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Computador'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ex.: Insira qualquer descrição do tipo de ativo aqui.'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance

class AssetModelForms(forms.ModelForm):
    form_name = 'Novo Modelo de Ativo'

    class Meta:
        model = AssetModel
        exclude = []
        labels = {
            'nome': 'Nome',
            'fabricante': 'Fabricante',
            'descricao': 'Descrição',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Computador'}),
            'fabricante': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ex.: Insira qualquer descrição do tipo de ativo aqui.'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class LocationForms(forms.ModelForm):
    form_name = 'Nova Localização'

    class Meta:
        model = Location
        exclude = []
        labels = {
            'nome': 'Nome',
            'local_pai': 'Local Pai',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Shop Bum'}),
            'local_pai': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(LocationForms, self).__init__(*args, **kwargs)
        self.fields['local_pai'].queryset = Location.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class MaintenanceForms(forms.ModelForm):
    form_name = 'Registro de Manutenção'

    class Meta:
        model = Maintenance
        exclude = []
        labels = {
            'ativo': 'Ativo em Manutenção',
            'data_inicio': 'Data de Entrada',
            'data_fim': 'Data de Conclusão',
            'descricao': 'Descrição',
            'custo': 'Custo de Manutenção'

        }
        widgets = {
            'ativo': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ex.: Shop Bum'}),
            'data_inicio': forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_fim': forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ex.: Insira qualquer informação sobre manutenção.'}),
            'custo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: R$ 100.50'}),
        }

    def save(self, commit=True):
        instance = super(MaintenanceForms, self).save(commit=False)
        if commit:
            instance.save()

        return instance


class AssetForms(forms.ModelForm):
    form_name = 'Novo Ativo'

    class Meta:
        model = Asset
        exclude = []
        labels = {
            'nome': 'Nome',
            'tipo': 'Tipo',
            'numero_serie': 'Número de Série',
            'patrimonio': 'Número de Patrimônio',
            'data_aquisicao': 'Data de Aquisiçaõ',
            'valor_aquisicao': 'Valor de Aquisição',
            'fabricante': 'Fabricante',
            'site': 'Site (destino)',
            'localizacao': 'Localização',
            'centro_de_custo': 'Centro de Custo',
            'status': 'Status'
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: RQE-100200-DT'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: XX001Y67P'}),
            'patrimonio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 100200'}),
            'data_aquisicao': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_aquisicao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: R$ 1000.00'}),
            'fabricante': forms.Select(attrs={'class': 'form-control'}),
            'centro_de_custo': forms.Select(attrs={'class': 'form-control'}),
            'site': forms.Select(attrs={'class': 'form-control'}),
            'localizacao': forms.Select(attrs={'class': 'form-control'}),
            'centro_de_custo': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class LoanForms(forms.ModelForm):
    form_name = 'Novo Empréstimo'


    class Meta:
        model = Loan
        exclude = ['status']
        fields = ['usuario', 'centro_de_custo', 'data_emprestimo',
            'data_devolucao_prevista', 'data_devolucao_real',
            'chamado_top_desk',  'observacoes',]
        labels = {
            'usuario': 'Usuário Responsável',
            'ativos': 'Ativos Emprestados',
            'centro_de_custo': 'Centro de Custo',
            'data_emprestimo': 'Data de Empréstimo',
            'data_devolucao_prevista': 'Data de Devolução Prevista',
            'data_devolucao_real': 'Data de Devolução Real',
            'chamado_top_desk': 'Chamado Relacionado',
            'observacoes': 'Observação',
        }
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'centro_de_custo': forms.Select(attrs={'class': 'form-control'}),
            'data_emprestimo': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_devolucao_prevista': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_devolucao_real': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'chamado_top_desk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: I2305-XXX'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Aqui você pode inserir qualquer observação sobre o empréstimo. Como por exemplo: justificativas, registros futuros e etc.'}),
        }


    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
            
            self.save_m2m(instance)

        return instance
    
    def save_m2m(self, instance):
        assets = self.cleaned_data['assets']
        for asset in assets:
            LoanAsset.objects.create(ativo=asset, emprestimo=instance)