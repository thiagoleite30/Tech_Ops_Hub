from django.shortcuts import render
from apps.tech_assets.context_processors import get_profile_foto
from apps.tech_assets.models import Approval, Asset, AssetCart, Cart
from apps.tech_assets.services import register_logentry
from django.contrib.admin.models import CHANGE, DELETION, ADDITION
from django.shortcuts import get_object_or_404, render, redirect
from apps.tech_assets.forms import AssetModelForms, LoanForms, AssetForms, MaintenanceForms, \
    LocationForms, ManufacturerForms, CostCenterForms, \
    AssetTypeForms
from django.urls import resolve
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Q
from django.core.paginator import Paginator

# Create your views here.


def login(request):
    return render(request, 'shared/login.html')


@login_required
def index(request):
    return render(request, 'apps/tech_assets/index.html')


@login_required
def cadastro_fabricante(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = ManufacturerForms

    if request.method == 'POST':
        form = ManufacturerForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(
                usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_fabricante')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
def cadastro_modelo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = AssetModelForms

    if request.method == 'POST':
        form = AssetModelForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(
                usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_modelo')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
def cadastro_centro_custo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = CostCenterForms

    if request.method == 'POST':
        form = CostCenterForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(
                usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_centro_custo')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
def cadastro_tipo_ativo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = AssetTypeForms

    if request.method == 'POST':
        form = AssetTypeForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(
                usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_tipo_ativo')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
def cadastro_local(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = LocationForms

    if request.method == 'POST':
        form = LocationForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(
                usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_local')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
def cadastro_manutencao(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = MaintenanceForms

    if request.method == 'POST':
        form = MaintenanceForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(
                usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_manutencao')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
def cadastro_ativo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = AssetForms

    if request.method == 'POST':
        form = AssetForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(),
                              action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_ativo')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
def novo_emprestimo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = LoanForms

    print(f'DEBUG :: VIEW :: CADASTRO ATIVO :: {form.form_name}')

    if request.method == 'POST':
        form = LoanForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(
                usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('novo_emprestimo')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
def ativos(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Instancia um subquery que trará uma lista de ativos \
        # que já estão em carrinho
    subquery = AssetCart.objects.filter(ativo_id=OuterRef('pk')).values('pk')

    # Captura a lista dos objetos já em um carrinho
    assets_in_cart = [
        asset.id for asset in Asset.objects.filter(Exists(subquery))]

    # Define um objeto request para capturar informação q ou vazio '' da url
    query = request.GET.get('q', '')

    # Obtém todos os assets cadastrados
    assets = Asset.objects.all()

    # Estrutura lógica na view de ativos para modificar os assets de acordo \
    # com a consulta obtida na query
    if query:
        assets = assets.filter(
            Q(nome__icontains=query) |
            Q(patrimonio__icontains=query)
        )

    # Uma instancia paginator definida para o máximo de 15 ativos por pagina \
        # E já captura dos assets os 15 primeiros da consulta
    paginator = Paginator(assets, 15)

    # Obtém o número da página atual
    page_number = request.GET.get('page')

    # Obtém os objetos de acordo com a página presente no URL
    page_obj = paginator.get_page(page_number)

    print(f'DEBUG :: VIEW :: CARRINHO :: PAGE OBJ :: {page_obj}')

    return render(request, 'apps/tech_assets/ativos.html', {'assets_in_cart': assets_in_cart, 'page_obj': page_obj, 'query': query})


@login_required
def carrinho(request):
    if not request.user.is_authenticated:
        return redirect('login')

    subquery = AssetCart.objects.filter(ativo_id=OuterRef('pk')).values('pk')
    query = request.GET.get('q', '')

    # Obtenha o carrinho do usuário logado
    cart = get_object_or_404(Cart, usuario_sessao=request.user)

    # Recupere os itens do carrinho do usuario logado
    cart_items = AssetCart.objects.filter(carrinho=cart)

    # Crie uma lista com is ids dos ativos no carrinho
    ids_assets_in_cart = [item.ativo_id for item in cart_items]

    # Busca na tabela asset todos os ids na lista acima
    assets = Asset.objects.filter(id__in=ids_assets_in_cart)

    # Query pode ser alterada dependendo de como queremos consultar
    if query:
        assets = assets.filter(
            Q(nome__icontains=query) |
            Q(patrimonio__icontains=query)
        )

    paginator = Paginator(assets, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print(f'DEBUG :: VIEW :: CARRINHO :: PAGE OBJ :: {page_obj}')

    # Passe os dados para o template
    context = {
        'page_obj': page_obj,
        'query': query
    }

    print(f"ASSETS: {len(assets)}")

    # Redireciona para a lista de itens
    return render(request, 'apps/tech_assets/carrinho_cards.html', context)


@login_required
def add_carrinho(request, asset_id):
    if not request.user.is_authenticated:
        return redirect('login')

    # Assume que o usuário está autenticado
    asset = get_object_or_404(Asset, id=asset_id)
    user_instance = get_object_or_404(User, username=request.user)

    if asset:
        # Verifique se já existe um carrinho para este usuário ou crie um novo
        cart, created = Cart.objects.get_or_create(
            usuario_sessao=user_instance)

        # Verifique se o asset já está no carrinho
        asset_cart, created = AssetCart.objects.get_or_create(
            ativo=asset,
            carrinho=cart
        )
        if created:
            # O asset foi adicionado ao carrinho
            print(f"Asset {asset_id} adicionado ao carrinho.")
            return redirect('ativos')
        else:
            # O asset já estava no carrinho
            print(f"Asset {asset_id} já está no carrinho.")
            return redirect('ativos')
    return redirect('index')


@login_required
def remove_do_carrinho(request, asset_id):
    if not request.user.is_authenticated:
        return redirect('login')

    # Pega da tabela asset o ativo pelo id
    asset = get_object_or_404(Asset, id=asset_id)
    
    # Pega a instancia do usuário logado
    user_instance = get_object_or_404(User, username=request.user)

    # Se houver asset
    if asset:
        try:
            cart = get_object_or_404(Cart, usuario_sessao=user_instance)
            if cart:
                asset_cart = get_object_or_404(
                    AssetCart, ativo=asset, carrinho=cart)
                if asset_cart:
                    asset_cart.delete()
                return redirect('carrinho')
        except Exception as e:
            print(f'ERROR :: REMOVE CARRINHO :: {e}')

    return redirect('index')


@login_required
def deleta_carrinho(request):
    if not request.user.is_authenticated:
        return redirect('login')

    
    # Pega a instancia do usuário logado
    user_instance = get_object_or_404(User, username=request.user)

    # Se houver usuario
    if user_instance:
        try:
            cart = get_object_or_404(Cart, usuario_sessao=user_instance)
            if cart:
                assets_cart = AssetCart.objects.filter(carrinho=cart)
                if assets_cart:
                    assets_cart.delete()
                return redirect('carrinho')
        except Exception as e:
            print(f'ERROR :: DELETA CARRINHO :: {e}')

    return redirect('index')