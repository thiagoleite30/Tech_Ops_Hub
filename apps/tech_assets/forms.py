from django import forms
from django.db import connection
from django.shortcuts import get_object_or_404
from apps.tech_assets.models import Asset, AssetCart, AssetModel, Cart, Manufacturer, CostCenter, \
    AssetType, Location, Maintenance, Movement, MovementAsset
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.contrib.admin.models import CHANGE, DELETION, ADDITION

from apps.tech_assets.services import register_logentry


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
        else:
            raise forms.ValidationError()

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
        else:
            raise forms.ValidationError()

        return instance


class AssetTypeForms(forms.ModelForm):
    form_name = 'Novo Tipo de Ativo'

    nome = forms.CharField(
        label="Nome",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Notebook'
            }
        )
    )

    class Meta:
        model = AssetType
        exclude = []
        fields = ['nome', 'descricao',]
        labels = {
            'descricao': 'Descrição',
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ex.: Insira qualquer descrição do tipo de ativo aqui.'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        else:
            raise forms.ValidationError()

        return instance

    def clean_nome(self):
        if 'nome' not in self.cleaned_data:
            raise forms.ValidationError(
                f'Campo "{nome}" não encontrado nos dados limpos.')
        nome = self.cleaned_data['nome']
        if nome:
            nome_exist = [
                t.nome for t in AssetType.objects.filter(nome__iexact=nome)]
            if nome_exist:
                raise forms.ValidationError(
                    f'O nome "{nome}" já está em uso com "{nome_exist[0]}".')

        return nome


class AssetModelForms(forms.ModelForm):
    form_name = 'Novo Modelo de Ativo'

    class Meta:
        model = AssetModel
        exclude = []
        labels = {
            'tipo': 'Tipo de Ativo',
            'nome': 'Nome',
            'fabricante': 'Fabricante',
            'descricao': 'Descrição',
        }
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Computador'}),
            'fabricante': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ex.: Insira qualquer descrição do tipo de ativo aqui.'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        else:
            raise forms.ValidationError()

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
        else:
            raise forms.ValidationError()

        return instance


class MaintenanceForms(forms.ModelForm):
    form_name = 'Registro de Manutenção'

    operador = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}),
        required=True
    )

    if 'tipo' == 'interna':
        print(f'Manutenção interna!!!')

    class Meta:
        model = Maintenance
        exclude = ['status', 'dias_atraso', 'data_fim']
        labels = {
            'tipo_manutencao': 'Tipo de Manutenção',
            'ativo': 'Ativo em Manutenção',
            'data_inicio': 'Data de Entrada',
            'data_prevista_fim': 'Previsão de Conclusão',
            'data_fim': 'Data de Conclusão',
            'chamado_top_desk': 'Chamado Interno',
            'chamado_externo': 'Chamado Externo',
            'descricao': 'Descrição',
            'custo': 'Custo de Manutenção'
        }
        widgets = {
            'tipo_manutencao': forms.Select(attrs={'class': 'form-control'}),
            'ativo': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ex.: Shop Bum'}),
            'data_inicio': forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_prevista_fim': forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'},),
            'data_fim': forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}),
            'chamado_top_desk': forms.TextInput(attrs={'class': 'form-control'}),
            'chamado_externo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ex.: Insira qualquer informação sobre manutenção.'}),
            'custo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: R$ 100.50'}),
        }

    def clean_operador(self):
        operador = self.cleaned_data.get('operador')

        if not operador:
            raise forms.ValidationError()
        return operador
    
    def clean_data_prevista_fim(self):
        data_inicio = self.cleaned_data.get('data_inicio')
        data_prevista_fim = self.cleaned_data.get('data_prevista_fim')

        if not data_prevista_fim:
            raise forms.ValidationError(message=f'Uma previsão de fim de manutenção dever ser passada!')
        if data_inicio > data_prevista_fim:
            raise forms.ValidationError(message=f'A data prevista para conclusão não pode ser inferior a data de inicio!')
        
        return data_prevista_fim
    
    def clean_chamado_externo(self):
        chamado_externo = self.cleaned_data.get('chamado_externo')
        tipo_manutencao = self.cleaned_data.get('tipo_manutencao')
        
        if tipo_manutencao == 'externa' and not chamado_externo:
            raise forms.ValidationError(message=f'Um número de chamado externo deve ser informado para manutenções Externas!')
        
        return chamado_externo
            

    def __init__(self, *args, **kwargs):
        # Receber a lista de ativos a ser preenchida
        ativo = kwargs.pop('ativo', None)
        super().__init__(*args, **kwargs)
        if ativo is not None:
            self.fields['ativo'].queryset = Asset.objects.filter(pk=ativo)
            self.fields['ativo'].initial = ativo
            self.fields['ativo'].widget.attrs['readonly'] = False

    def save(self, commit=True):
        instance = super(MaintenanceForms, self).save(commit=False)
        ativo_nome = self.cleaned_data.get('ativo')
        if commit:
            try:
                instance.save()
                ativo = get_object_or_404(Asset, nome=ativo_nome)
                ativo.status = 'em_manutencao'
                ativo.save()
            except Exception as e:
                raise forms.ValidationError(
                    f"Erro ao salvar a manutenção: {str(e)}")

        else:
            raise forms.ValidationError(
                "O formulário não foi salvo corretamente.")

        return instance


class AssetForms(forms.ModelForm):
    form_name = 'Novo Ativo'

    class Meta:
        model = Asset
        exclude = ['status']
        fields = ['tipo', 'modelo', 'nome', 'numero_serie',
                  'patrimonio', 'data_aquisicao', 'valor_aquisicao',
                  'localizacao',]
        labels = {
            'nome': 'Nome',
            'tipo': 'Tipo',
            'modelo': 'Modelo',
            'numero_serie': 'Número de Série',
            'patrimonio': 'Número de Patrimônio',
            'data_aquisicao': 'Data de Aquisiçaõ',
            'valor_aquisicao': 'Valor de Aquisição',
            'localizacao': 'Localização',
            'status': 'Status'
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: RQE-100200-DT'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'modelo': forms.Select(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: XX001Y67P'}),
            'patrimonio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 100200'}),
            'data_aquisicao': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_aquisicao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: R$ 1000.00'}),
            'localizacao': forms.Select(attrs={'class': 'form-control'}),
            'centro_de_custo': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        
            

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        else:
            raise forms.ValidationError()

        return instance
    

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome:
            nome_exist = [asset.nome for asset in Asset.objects.filter(nome__iexact=nome)]
            if nome_exist:
                raise forms.ValidationError(
                    f'O nome "{nome}" já está em uso com "{nome_exist[0]}".')

        return nome

class MovementForms(forms.ModelForm):
    form_name = 'Nova Movimentação'

    ativos = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.none(),
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control'}),
        required=False
    )


    aprovador = forms.ModelChoiceField(
            queryset=Group.objects.none(),
            widget=forms.Select(
                attrs={'class': 'form-control'}),
            required=True
        )

    class Meta:
        model = Movement
        exclude = ['status', 'data_devolucao_real']
        fields = ['tipo', 'usuario', 'centro_de_custo', 'aprovador', 'data_movimento',
                  'data_devolucao_prevista',
                  'chamado_top_desk',  'observacoes', 'ativos']
        labels = {
            'tipo': 'Tipo de Movimentação',
            'usuario': 'Usuário Recebedor',
            'ativos': 'Ativos Selecionados',
            'centro_de_custo': 'Centro de Custo',
            'data_movimento': 'Data de Início',
            'data_devolucao_prevista': 'Data de Devolução Prevista',
            'data_devolucao_real': 'Data de Devolução Real',
            'chamado_top_desk': 'Chamado Relacionado',
            'observacoes': 'Observação',
        }
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'centro_de_custo': forms.Select(attrs={'class': 'form-control'}),
            'data_movimento': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_devolucao_prevista': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_devolucao_real': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'chamado_top_desk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: I2305-XXX'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Aqui você pode inserir qualquer observação sobre o empréstimo. Como por exemplo: justificativas, registros futuros e etc.'}),
        }

    def __init__(self, *args, **kwargs):
        # Receber a lista de ativos a ser preenchida
        ativos = kwargs.pop('ativos', None)
        aprovador = kwargs.pop('aprovador', None)
        
        super().__init__(*args, **kwargs)
        if ativos is not None:
            self.fields['ativos'].queryset = Asset.objects.filter(
                id__in=[a.id for a in ativos])
            self.fields['ativos'].initial = ativos
            self.fields['ativos'].widget.attrs['readonly'] = False
        if 'auth_group' in connection.introspection.table_names():
            grupo = get_object_or_404(Group, name='Aprovadores TI')
            users = grupo.user_set.all()
            self.fields['aprovador'].queryset = users
            self.fields['aprovador'].initial = aprovador
            self.fields['aprovador'].widget.attrs['readonly'] = False
            

    def clean_ativos(self):
        ativos = self.cleaned_data['ativos']
        if ativos:
            for asset in ativos:
                if MovementAsset.objects.filter(ativo=asset, movimento__status__in=['pendente_aprovação', 'em_andamento', 'atrasado']).exists():
                    raise forms.ValidationError(
                        f'O ativo {asset} já está em uma movimentação de ativos.')
                else:
                    return ativos
        else:
            raise forms.ValidationError(
                f'Nenhum ativo selecionado. Verifique o carrinho!')

    def clean_data_devolucao_prevista(self):
        data_movimento = self.cleaned_data.get('data_movimento')
        data_devolucao_prevista = self.cleaned_data.get('data_devolucao_prevista')
        
        if data_devolucao_prevista:
            if data_movimento > data_devolucao_prevista:
                raise forms.ValidationError(message=f'A data prevista para devolução não pode ser inferior a data de inicio!')
        
        return data_devolucao_prevista

    def save(self, commit=True):
        instance = super().save(commit=False)
        ativos = self.cleaned_data['ativos']
        aprovador = self.cleaned_data['aprovador']
        if commit:
            instance.save(ativos=ativos, aprovador=aprovador)
        else:
            raise forms.ValidationError()

        return instance


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
