import traceback
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.urls import resolve
from django.contrib.admin.models import ADDITION
from django.contrib import messages
from apps.move_gpos.forms import RequestForms
from apps.move_gpos.models import GPOS, Request
from apps.move_gpos.services import dispara_fluxo, dispara_fluxo_debug
from apps.tech_assets.models import AssetInfo, Location
from apps.tech_assets.services import register_logentry
from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Q, Case, \
    When, Value, IntegerField
from django.core.paginator import Paginator
from utils.decorators import group_required

# Create your views here.


@login_required
@group_required(['Suporte', 'Move GPOS', 'Administradores'], redirect_url='zona_restrita')
def move_gpos(request):

    return render(request, 'apps/move_gpos/move_gpos.html')


@login_required
@group_required(['Suporte', 'Move GPOS', 'Administradores'], redirect_url='zona_restrita')
def get_pdvs(request):
    pdvs_list = []
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


@login_required
@group_required(['Suporte', 'Move GPOS', 'Administradores'], redirect_url='zona_restrita')
def solicitacoes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_instance = get_object_or_404(User, username=request.user)

    if user_instance:
        try:
            query = request.GET.get('q', '')
            solicitacoes = Request.objects.select_related('gpos', 'pdv_atual', 'loja_nova', 'pdv_novo', 'usuario').filter(usuario__username=user_instance)
            default_status = False
            status_solicitacao = request.GET.getlist('status')

            if query:
                solicitacoes = solicitacoes.filter(
                    Q(id__icontains=query) |
                    Q(chamado__icontains=query) |
                    Q(gpos__ativo__nome__icontains=query) |
                    Q(gpos__loja__nome__icontains=query) |
                    Q(pdv_atual__nome__icontains=query) |
                    Q(pdv_novo__nome__icontains=query) |
                    Q(usuario__username__icontains=query) |
                    Q(usuario__first_name__icontains=query) |
                    Q(usuario__last_name__icontains=query)
                 )

            status_query = Q()
            if status_solicitacao:
                if 'concluido' in status_solicitacao:
                    status_query |= Q(concluida=True)
                if 'pendente' in status_solicitacao:
                    status_query |= Q(concluida=False)

            solicitacoes = solicitacoes.filter(status_query).order_by(
                Case(
                    When(concluida=False, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                ),
                'concluida',
                '-data_inclusao',
            )

            paginator = Paginator(solicitacoes, 16)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                #'solicitacoes': solicitacoes,
                'url_form': resolve(request.path_info).url_name,
                'page_obj': page_obj,
                'query': query,
            }

            return render(request, 'apps/move_gpos/solicitacoes.html', context)
        except Exception as e:
            print(f'ERROR :: SOLICITAÇÕES :: {e}')
            traceback.print_exc()

    return redirect('index')