from .models import Approval, Cart, AssetCart, Termo
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


def verifica_movimentacoes(request):
    if request.user.is_authenticated:
        minhas_movimentacoes = Termo.objects.select_related(
                'movimentacao', 'aprovacao').filter(movimentacao__usuario=request.user).exists()
        print(f'\n\nDEBUG :: VERIFICA MOVIMENTACOES MINHAS :: {minhas_movimentacoes}')
        return {'minhas_movimentacoes': minhas_movimentacoes}
    return {'minhas_movimentacoes': False}

def verifica_minhas_aprovacoes_pendentes(request):
    if request.user.is_authenticated:
        minhas_aprovacoes_pendentes = Approval.objects.filter(movimentacao__usuario=request.user, status_aprovacao='pendente').exists()
        return {'minhas_aprovacoes_pendentes': minhas_aprovacoes_pendentes}
    return {'minhas_aprovacoes_pendentes': False}

def verifica_aprovacoes_pendentes(request):
    if request.user.is_authenticated:
        aprovacoes_pendentes = Approval.objects.filter(
            status_aprovacao='pendente').exists()
        return {'aprovacoes_pendentes': aprovacoes_pendentes}
    return {'aprovacoes_pendentes': False}


def get_profile_info(request):
    if request.user.is_authenticated:
        if 'profile_photo' not in request.session:
            foto = get_user_photo_microsoft(request.user)
            request.session['profile_photo'] = foto
        else:
            foto = request.session['profile_photo']
        
    else:
        foto = None
    return {'profile_photo': foto}

# Controles permissivos


def user_groups_processor(request):
    if request.user.is_authenticated:
        # Carrega todos os grupos de uma vez usando prefetch_related
        groups = list(request.user.groups.values_list('name', flat=True))
    else:
        groups = []
    
    return {'user_groups': groups}