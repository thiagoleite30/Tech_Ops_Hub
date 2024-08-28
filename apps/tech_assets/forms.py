from django import forms
from django.db import connection
from django.shortcuts import get_object_or_404
from apps.tech_assets.models import Accessory, Approval, Asset, AssetCart, AssetModel, Cart, Manufacturer, CostCenter, \
    AssetType, Location, Maintenance, Movement, MovementAccessory, MovementAsset, ReturnTerm
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.contrib.admin.models import CHANGE, DELETION, ADDITION
from django.db.models import Q

from apps.tech_assets.services import register_logentry


class MovementAccessoryForm(forms.ModelForm):
    class Meta:
        model = MovementAccessory
        fields = ['acessorio', 'quantidade']
        labels = {
            'acessorio': 'Acessório',
            'quantidade': 'Quantidade'
        }
        widgets = {
            'acessorio': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
        }


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


class AccessoryForms(forms.ModelForm):
    form_name = 'Novo Acessório'

    class Meta:
        model = Accessory
        exclude = []
        labels = {
            'nome': 'Nome',
            'modelo': 'Modelo',
            'tipo': 'Tipo',
            'fabricante': 'Fabricante',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fabricante': forms.Select(attrs={'class': 'form-control'}),
        }


class MaintenanceForms(forms.ModelForm):
    form_name = 'Registro de Manutenção'

    operador = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}),
        required=True
    )

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
            raise forms.ValidationError(
                message=f'Uma previsão de fim de manutenção dever ser passada!')
        if data_inicio > data_prevista_fim:
            raise forms.ValidationError(
                message=f'A data prevista para conclusão não pode ser inferior a data de inicio!')

        return data_prevista_fim

    def clean_chamado_externo(self):
        chamado_externo = self.cleaned_data.get('chamado_externo')
        tipo_manutencao = self.cleaned_data.get('tipo_manutencao')

        if tipo_manutencao == 'externa' and not chamado_externo:
            raise forms.ValidationError(
                message=f'Um número de chamado externo deve ser informado para manutenções Externas!')

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
            'centro_de_custo_recebedor': forms.Select(attrs={'class': 'form-control'}),
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
            nome_exist = [
                asset.nome for asset in Asset.objects.filter(nome__iexact=nome)]
            if nome_exist:
                raise forms.ValidationError(
                    f'O nome "{nome}" já está em uso com "{nome_exist[0]}".')

        return nome


class DynamicAccessoryForm(forms.Form):
    acessorio = forms.ModelChoiceField(
        queryset=Accessory.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        required=False
    )

    quantidade = forms.IntegerField(
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']

        if quantidade:
            if quantidade <= 0:
                raise forms.ValidationError(
                    message="A quantidade informada tem que ser maior que 0 (zero)!")
        return quantidade


DynamicAccessoryFormSet = forms.formset_factory(
    DynamicAccessoryForm, extra=0, can_delete=True)


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

    accessories_data = forms.CharField(
        widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Movement
        exclude = ['status', 'data_devolucao_real']
        fields = ['tipo', 'usuario_cedente', 'centro_de_custo_cedente', 'usuario', 'centro_de_custo_recebedor', 'aprovador', 'data_movimento',
                  'data_devolucao_prevista',
                  'chamado_top_desk',  'observacoes', 'ativos']
        labels = {
            'tipo': 'Tipo de Movimentação',
            'usuario_cedente': 'Usuário Cedente',
            'centro_de_custo_cedente': 'Centro de Custo Cedente',
            'usuario': 'Usuário Recebedor',
            'centro_de_custo_recebedor': 'Centro de Custo Cedente',
            'data_movimento': 'Data de Início',
            'data_devolucao_prevista': 'Data de Devolução Prevista',
            'data_devolucao_real': 'Data de Devolução Real',
            'chamado_top_desk': 'Chamado Relacionado',
            'ativos': 'Ativos Selecionados',
            'observacoes': 'Observação',
        }
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'usuario_cedente': forms.Select(attrs={'class': 'form-control'}),
            'centro_de_custo_cedente': forms.Select(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'centro_de_custo_recebedor': forms.Select(attrs={'class': 'form-control'}),
            'data_movimento': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_devolucao_prevista': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_devolucao_real': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'chamado_top_desk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: I2305-XXX'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Aqui você pode inserir qualquer observação sobre o empréstimo. Como por exemplo: justificativas, registros futuros e etc.'}),
        }

    def __init__(self, *args, **kwargs):
        # Receber a lista de ativos a ser preenchida
        # sub_form_instance = kwargs.pop('sub_form_instance', None)
        ativos = kwargs.pop('ativos', None)
        aprovador = kwargs.pop('aprovador', None)
        formset = kwargs.pop('formset', None)
        # Configure o formulário secundário
        super().__init__(*args, **kwargs)
        self.formset = formset if formset else DynamicAccessoryFormSet()
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
        quantidades = self.data.getlist('form-quantidade')
        if ativos:
            for asset in ativos:
                if MovementAsset.objects.filter(ativo=asset, movimento__status__in=['pendente_aprovação', 'em_andamento', 'atrasado']).exists():
                    raise forms.ValidationError(
                        f'O ativo {asset} já está em uma movimentação de ativos.')
                else:
                    return ativos
        elif not quantidades:
            raise forms.ValidationError(
                f'Nenhum ativo e/ou acessório esta contido na movimentação.')

    def clean_data_devolucao_prevista(self):
        data_movimento = self.cleaned_data.get('data_movimento')
        data_devolucao_prevista = self.cleaned_data.get(
            'data_devolucao_prevista')

        if data_devolucao_prevista:
            if data_movimento > data_devolucao_prevista:
                raise forms.ValidationError(
                    message=f'A data prevista para devolução não pode ser inferior a data de inicio!')

        return data_devolucao_prevista

    def clean_accessories_data(self):
        # Supondo que você está coletando os dados diretamente dos campos do formset
        quantidades = self.data.getlist('form-quantidade')

        for quantity in quantidades:
            try:
                if int(quantity) <= 0:
                    raise forms.ValidationError(
                        "A quantidade informada tem que ser maior que 0 (zero)!")
            except ValueError:
                raise forms.ValidationError("Quantidade inválida.")

        return self.cleaned_data.get('accessories_data')

    def save(self, commit=True):
        instance = super().save(commit=False)
        ativos = self.cleaned_data['ativos']
        aprovador = self.cleaned_data['aprovador']
        # Capture os acessórios enviados no POST
        acessorios_id = self.data.getlist('form-acessorio')
        quantidades = self.data.getlist('form-quantidade')

        # Verifique se as listas têm o mesmo comprimento
        if len(acessorios_id) != len(quantidades):
            raise ValueError(
                "O número de IDs de acessórios e quantidades não coincide.")

        # Agrupe IDs e some as quantidades
        accessory_quantity_map = {}
        for accessory_id, quantity in zip(acessorios_id, quantidades):
            if accessory_id in accessory_quantity_map:
                accessory_quantity_map[accessory_id] += int(quantity)
            else:
                accessory_quantity_map[accessory_id] = int(quantity)

        if commit:
            if ativos != None:
                instance.save(ativos=ativos, aprovador=aprovador,
                              acessorios=accessory_quantity_map)
            else:
                instance.save(aprovador=aprovador,
                              acessorios=accessory_quantity_map)

            # Processar os dados do formset
            for form in self.formset:
                if form.cleaned_data:
                    # Salvar ou processar os dados dos acessórios
                    pass

        else:
            raise forms.ValidationError()

        return instance


class ApprovalForms(forms.ModelForm):
    form_name = 'Aprovação'

    aprovador = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        widget=forms.Select(
            attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Approval
        exclude = ['ultima_modificacao', 'status_aprovacao', 'movimentacao']
        fields = ['aprovador', 'status_aprovacao', 'movimentacao',]
        labels = {
            'aprovador': 'Aprovador Designado',
        }
        widgets = {

            'status_aprovacao': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        aprovador = kwargs.pop('aprovador', None)
        super().__init__(*args, **kwargs)

        if 'auth_group' in connection.introspection.table_names():
            grupo = get_object_or_404(Group, name='Aprovadores TI')
            users = grupo.user_set.all()
            self.fields['aprovador'].queryset = users
            self.fields['aprovador'].initial = aprovador
            self.fields['aprovador'].widget.attrs['readonly'] = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class ReturnTermForms(forms.ModelForm):
    form_name = 'Termo de Devolução'

    class Meta:
        model = ReturnTerm
        exclude = ['movimentacao', 'data_retorno', 'status', 'usuario_recebedor']
        fields = ['observacao',]
        labels = {
            'observacao': 'Observações de entrega',
        }
        widgets = {
            'observacao': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True, *args, **kwargs):
        usuario_recebedor = kwargs.pop('user', None)
        instance = super().save(commit=False)
        if usuario_recebedor:
            instance.usuario_recebedor = usuario_recebedor

        if commit:
            instance.save()
        return instance

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
