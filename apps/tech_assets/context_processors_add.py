from .models import Approval, Cart, AssetCart
from django.contrib.auth.models import User
from apps.tech_assets.services import get_user_photo_microsoft, get_employedId
from django.conf import settings
from django.contrib.auth.models import Group


def cart_item_count(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(usuario_sessao=request.user)
        count = AssetCart.objects.filter(carrinho=cart).count()
    else:
        count = 0

    return {'cart_item_count': count}

def get_url_login_ms(request):
    return {'URL_POS_CLICK_MS_LOGO': settings.URL_POS_CLICK_MS_LOGO}

def get_url_logout(request):
    return {'URL_LOGOUT': settings.LOGOUT_REDIRECT_URL}


def verifica_aprovacoes_pendentes(request):
    if request.user.is_authenticated:
        aprovacoes_pendentes = Approval.objects.filter(movimentacao__usuario=request.user).exists()
        return {'aprovacoes_pendentes': aprovacoes_pendentes}
    return {'aprovacoes_pendentes': False}

def verifica_movimentacoes(request):
    minhas_movimentacoes = Approval.objects.filter(
        status_aprovacao='pendente').exists()
    return {'minhas_movimentacoes': minhas_movimentacoes}


def get_profile_info(request):
    if request.user.is_authenticated:
        if 'profile_photo' not in request.session:
            foto = get_user_photo_microsoft(request.user)
            request.session['profile_photo'] = foto
        else:
            foto = request.session['profile_photo']
        
        if 'employeeId' not in request.session:
            employeeId = get_employedId(request.user)
            request.session['employeeId'] = employeeId
        else:
            employeeId = request.session['employeeId']
        
    else:
        foto = None
        employeeId = None
    return {'profile_photo': foto, 'employeeId': employeeId}

# Controles permissivos


def user_groups_processor(request):
    if request.user.is_authenticated:
        # Carrega todos os grupos de uma vez usando prefetch_related
        groups = list(request.user.groups.values_list('name', flat=True))
    else:
        groups = []
    
    return {'user_groups': groups}

"""
def is_administradores_user(request):
    is_admin = False
    user = request.user
    if user.is_authenticated:
        is_admin = user.groups.filter(name='Administradores').exists()
    return {'is_admin_user': is_admin}


def is_aprovadores_ti_user(request):
    is_aprovadores_ti_user = False
    user = request.user
    if user.is_authenticated:
        is_aprovadores_ti_user = user.groups.filter(
            name='Aprovadores TI').exists()
    return {'is_aprovadores_ti_user': is_aprovadores_ti_user}

def is_suporte_user(request):
    is_suporte_user = False
    user = request.user
    if request.user.is_authenticated:
        is_suporte_user = user.groups.filter(
            name='Suporte').exists()
    return {'is_suporte_user': is_suporte_user}

def is_mvgpos_user(request):
    is_mvgpos_user = False
    user = request.user
    if request.user.is_authenticated:
        is_mvgpos_user = user.groups.filter(
            name='Move GPOS').exists()
    return {'is_mvgpos_user': is_mvgpos_user}
"""