from .models import Approval, Cart, AssetCart
from django.contrib.auth.models import User
from apps.tech_assets.services import get_user_photo_microsoft
from django.conf import settings

def cart_item_count(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(usuario_sessao=request.user)
        count = AssetCart.objects.filter(carrinho=cart).count()
    else:
        count = 0
    
    return {'cart_item_count': count}


def get_url_logout(request):   
    return {'URL_LOGOUT' : settings.LOGOUT_REDIRECT_URL}


def verifica_aprovacoes_pendentes(request):
    aprovacoes_pendentes = Approval.objects.filter(
        status_aprovacao='pendente').exists()
    return {'aprovacoes_pendentes': aprovacoes_pendentes}

def get_profile_foto(request):
    if request.user.is_authenticated:
        foto = get_user_photo_microsoft(request.user)
    else:
        foto = None
    return {'profile_photo' : foto}