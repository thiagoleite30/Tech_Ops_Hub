from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve
from django.contrib.admin.models import ADDITION
from django.contrib import messages
from apps.move_gpos.forms import RequestForms
from apps.move_gpos.models import GPOS
from apps.move_gpos.services import dispara_fluxo, dispara_fluxo_debug
from apps.tech_assets.models import AssetInfo, Location
from apps.tech_assets.services import register_logentry
from django.contrib.auth.decorators import login_required
from utils.decorators import group_required

# Create your views here.


@login_required
@group_required(['Suporte', 'Move GPOS', 'Administradores'], redirect_url='zona_restrita')
def move_gpos(request):

    return render(request, 'apps/move_gpos/move_gpos.html')


@login_required
@group_required(['Suporte', 'Move GPOS', 'Administradores'], redirect_url='zona_restrita')
def get_pdvs(request):
    if request.GET.get('gpos_id'):
        gpos_id = request.GET.get('gpos_id')
        gpos = GPOS.objects.get(pk=gpos_id)
        gpos_queryset = GPOS.objects.filter(pos_number=gpos.pos_number,
                                            primary_pdv=False,
                                            blocked=False,
                                            active=True
                                            ).select_related(
                                                'ativo',
                                                'loja',
                                                'pdv'
        )
        if not gpos_queryset.exists():
            gpos_queryset = GPOS.objects.filter(pos_number=gpos.pos_number,
                                                primary_pdv=True,
                                                blocked=False,
                                                active=True
                                                ).select_related(
                                                    'ativo',
                                                    'loja',
                                                    'pdv'
            )

        list_locations = [obj.pdv for obj in gpos_queryset]
        pdvs_ids = [pdv.id for pdv in list_locations]
        pdvs_list = list(Location.objects.prefetch_related('local_pai').filter(
            id__in=pdvs_ids).values('id', 'nome'))
    elif request.GET.get('loja_id'):
        loja_id = request.GET.get('loja_id')
        loja = Location.objects.get(pk=loja_id)
        loja_queryset = Location.objects.prefetch_related('local_pai').filter(
            local_pai=loja)
        pdvs_list = list(loja_queryset.values('id', 'nome'))

    return JsonResponse(pdvs_list, safe=False)


@login_required
@group_required(['Suporte', 'Move GPOS', 'Administradores'], redirect_url='zona_restrita')
def get_gpos(request):
    gpos_queryset = GPOS.objects.filter(
        blocked=False
    ).select_related(
        'ativo',
        'loja',
        'pdv'
    ).order_by(
        'pos_number'
    ).distinct(
        'pos_number'
    )

    gpos_list = list(gpos_queryset.values('id', 'pos_number'))

    return JsonResponse(gpos_list, safe=False)


@login_required
@group_required(['Suporte', 'Move GPOS', 'Administradores'], redirect_url='zona_restrita')
def requisicao_troca(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = RequestForms()

    if request.method == 'POST':

        gpos = GPOS.objects.select_related(
            'ativo',
            'ativo__assetinfo',
            'loja',
            'pdv'
        ).all()
        
        form = RequestForms(request.POST)
        if form.is_valid():
            posNumber = form.cleaned_data.get('gpos')
            oldPDV = form.cleaned_data.get('pdv_atual')
            newPDV = form.cleaned_data.get('pdv_novo')

            instance = form.save(commit=False)
            instance.existe_novo_pdv = gpos.filter(
                pdv=newPDV, pos_number=posNumber.pos_number).exists()


            posIMEI = posNumber.ativo.assetinfo.get().endereco_mac
            json = {
                "posNumber": f'POS {posNumber.pos_number}',
                "posIMEI": posIMEI,
                "newPDV": newPDV.nome,
                "oldPDV": oldPDV.nome,
                "posHaveInNewPDV": instance.existe_novo_pdv,
                "posTypeId": 1 if posNumber.is_mac else 0,
                "chamado": ""
            }

            response = dispara_fluxo(request, json)
            instance.chamado = response[1] if response else None
            instance.usuario = request.user
            if response:
                register_logentry(instance=instance, action=ADDITION, user=request.user)
                instance.save()

            return redirect('move_gpos')

        else:
            for field, errors in form.errors.items():
                print(form)
                for error in errors:
                    messages.warning(request, message=error)
                    pass

    context = {
        'form': form,
        'url_form': resolve(request.path_info).url_name,
    }

    return render(request, 'apps/move_gpos/requisicao_troca.html', context)
