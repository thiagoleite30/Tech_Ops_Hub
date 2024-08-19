from .models import Approval, Cart, AssetCart
from django.contrib.auth.models import User
from apps.tech_assets.services import get_user_photo_microsoft
from django.conf import settings
from django.contrib.auth.models import Group


def cart_item_count(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(usuario_sessao=request.user)
        count = AssetCart.objects.filter(carrinho=cart).count()
    else:
        count = 0

    return {'cart_item_count': count}


def get_url_logout(request):
    return {'URL_LOGOUT': settings.LOGOUT_REDIRECT_URL}


def verifica_aprovacoes_pendentes(request):
    aprovacoes_pendentes = Approval.objects.filter(
        status_aprovacao='pendente').exists()
    return {'aprovacoes_pendentes': aprovacoes_pendentes}


def get_profile_foto(request):
    if request.user.is_authenticated:
        if 'profile_photo' not in request.session:
            # Buscar a foto e salvar na sessão
            foto = get_user_photo_microsoft(request.user)
            request.session['profile_photo'] = foto
        else:
            # Recuperar a foto da sessão
            foto = request.session['profile_photo']
    else:
        foto = None
    return {'profile_photo': foto}

# Controles permissivos


def is_administradores_user(request):
    is_admin = False
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='Administradores').exists()
    return {'is_admin_user': is_admin}


def is_aprovadores_user(request):
    is_aprovadores_user = False
    if request.user.is_authenticated:
        is_aprovadores_user = request.user.groups.filter(
            name='Aprovadores TI').exists()
    return {'is_aprovadores_user': is_aprovadores_user}
