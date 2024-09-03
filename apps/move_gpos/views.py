from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve

from apps.move_gpos.forms import RequestForms
from apps.move_gpos.models import GPOS
from apps.tech_assets.models import Location

# Create your views here.


def move_gpos(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    gpos = GPOS.objects.filter(blocked=False)
    form = RequestForms()
    
    if gpos:
        pdvs = [pdv.pdv for pdv in gpos]
    
    
    context = {
        'form': form,
        'url_form': resolve(request.path_info).url_name,
        'gpos':gpos,
        'pdvs':pdvs
        }
    
    return render(request, 'apps/move_gpos/move_gpos.html', context)

def get_pdvs(request):
    if request.GET.get('gpos_id'):
        gpos_id = request.GET.get('gpos_id')
        gpos = GPOS.objects.get(pk=gpos_id)
        gpos_queryset = GPOS.objects.filter(pos_number=gpos.pos_number)
        pdvs_list = list(gpos_queryset.values('id', 'pdv__nome'))
    elif request.GET.get('loja_id'):
        loja_id = request.GET.get('loja_id')
        loja = Location.objects.get(pk=loja_id)
        loja_queryset = Location.objects.filter(local_pai=loja)
        pdvs_list = list(loja_queryset.values('id', 'nome'))
    
    return JsonResponse(pdvs_list, safe=False)

def get_gpos(request):

    gpos_queryset = GPOS.objects.filter(blocked=False).order_by('pos_number').distinct('pos_number')
    gpos_list = list(gpos_queryset.values('id', 'pos_number'))
    
    return JsonResponse(gpos_list, safe=False)


def requisicao_troca(request):
    return render(request, 'apps/move_gpos/move_gpos.html')