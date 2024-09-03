from django import forms

from apps.move_gpos.models import GPOS, Request
from apps.tech_assets.models import Location


class RequestForms(forms.ModelForm):
    form_name = 'Requisição de Troca'

    class Meta:
        model = Request
        exclude = ['chamado', 'concluida']
        labels = {
            'gpos': 'GPOS',
            'pdv_atual': 'PDV Atual',
            'loja_nova': 'Nova Loja',
            'pdv_novo': 'Novo PDV',
        }
        widgets = {
            'gpos': forms.Select(attrs={'class': 'form-control'}),
            'pdv_atual': forms.Select(attrs={'class': 'form-control'}),
            'loja_nova': forms.Select(attrs={'class': 'form-control'}),
            'pdv_novo': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gpos'].queryset = GPOS.objects.filter(blocked=False).order_by('pos_number').distinct('pos_number')
        self.fields['pdv_atual'].queryset = Location.objects.none()
        self.fields['loja_nova'].queryset = Location.objects.filter(sub_locations__isnull=False).distinct()
        self.fields['pdv_novo'].queryset = Location.objects.none()