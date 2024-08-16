from django.shortcuts import render
from apps.tech_assets.models import Approval, Asset, AssetCart, AssetInfo, AssetModel, AssetType, Cart, LoanAsset, Maintenance, Manufacturer
from apps.tech_assets.services import register_logentry, get_loan_asset, upload_assets
from django.contrib.admin.models import CHANGE, DELETION, ADDITION
from django.shortcuts import get_object_or_404, render, redirect
from apps.tech_assets.forms import AssetModelForms, CSVUploadForm, LoanForms, AssetForms, MaintenanceForms, \
    LocationForms, ManufacturerForms, CostCenterForms, \
    AssetTypeForms
from django.urls import resolve
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Q
from django.core.paginator import Paginator
from django.contrib import auth, messages
from utils.decorators import group_required

# Create your views here.


def login(request):
    return render(request, 'shared/login.html')


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
def index(request):
    return render(request, 'apps/tech_assets/index.html')


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
def cadastro_fabricante(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = ManufacturerForms

    if request.method == 'POST':
        form = ManufacturerForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(),
                              action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_fabricante')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
def cadastro_modelo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = AssetModelForms

    if request.method == 'POST':
        form = AssetModelForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(),
                              action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_modelo')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
def cadastro_centro_custo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = CostCenterForms

    if request.method == 'POST':
        form = CostCenterForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(),
                              action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_centro_custo')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
def cadastro_tipo_ativo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = AssetTypeForms

    if request.method == 'POST':
        form = AssetTypeForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(),
                              action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_tipo_ativo')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
# @group_required('Admin', redirect_url='forbidden_url')
def cadastro_local(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = LocationForms

    if request.method == 'POST':
        form = LocationForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(),
                              action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_local')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
def cadastro_manutencao(request, asset_id):
    if not request.user.is_authenticated:
        return redirect('login')

    form = MaintenanceForms(ativo=asset_id)

    asset = get_object_or_404(Asset, id=asset_id)
    if asset:
        if Maintenance.objects.filter(ativo_id=asset_id, status=True).exists():
            print(f'Já existe uma manutenção em aberto para este ativo')
            return redirect('ativo', asset_id=asset_id)

    if request.method == 'POST':
        form = MaintenanceForms(request.POST, request.FILES, ativo=asset_id)

        if form.is_valid():

            register_logentry(instance=form.save(),
                              action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_manutencao')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name, 'asset_id': asset_id})


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
def concluir_manutencao(request, asset_id):
    if not request.user.is_authenticated:
        return redirect('login')

    asset = get_object_or_404(Asset, id=asset_id)
    if asset:

        loan_exist = get_loan_asset(asset_id)
        if loan_exist['status']:
            asset.status = 'em_uso'
            asset.save()
            modificacao = f'Alterou status para "Em Uso"'
        else:
            asset.status = 'em_estoque'
            asset.save()
            modificacao = f'Alterou status para "Em Estoque"'
            register_logentry(instance=asset, action=CHANGE,
                              modificacao=modificacao, user=request.user)

        maintenance = get_object_or_404(Maintenance, ativo_id=1, status=True)
        if maintenance:
            print(f'DEBUG :: VIEW :: CONCLUIR MANUTENCAO :: MANUTENÇAO EXIST :: {
                  maintenance.id}')
            maintenance.status = False
            maintenance.save()
            modificacao = f'Alterou status para "False" (Não ativa)'
            register_logentry(instance=maintenance, action=CHANGE,
                              modificacao=modificacao, user=request.user)
        return redirect('ativo', asset_id=asset_id)
    return redirect('ativos')


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
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
@group_required(['Suporte'], redirect_url='forbidden_url')
def novo_emprestimo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Obtenha o carrinho do usuário logado
    cart = get_object_or_404(Cart, usuario_sessao=request.user)

    # Recupere os itens do carrinho do usuario logado
    cart_items = AssetCart.objects.filter(carrinho=cart)

    # Crie uma lista com is ids dos ativos no carrinho
    ids_assets_in_cart = [item.ativo_id for item in cart_items]

    # Busca na tabela asset todos os ids na lista acima
    assets = Asset.objects.filter(id__in=ids_assets_in_cart)

    form = LoanForms(ativos=assets)

    if request.method == 'POST':
        form = LoanForms(request.POST, request.FILES, ativos=assets)
        print(f'DEBUG :: VIEW :: PASSOU PRO IF :: {form.form_name}')

        if form.is_valid():
            emprestimo = form.save()
            # print(f'DEBUG :: VIEW :: Novo Emprestimo :: Emprestimo {emprestimo}')
            register_logentry(instance=emprestimo,
                              action=ADDITION, user=request.user)
            assets.update(status='em_uso')

            deleta_carrinho(request)

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('novo_emprestimo')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
def ativos(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Filtra os assets que não estão como Em Estoque (disponíveis)
    assets_unavailable = [
        asset.id for asset in Asset.objects.exclude(status__in=['em_estoque'])]
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

    context = {
        'assets_in_cart': assets_in_cart,
        'page_obj': page_obj,
        'query': query,
        'assets_unavailable': assets_unavailable,
    }
    return render(request, 'apps/tech_assets/ativos.html', context)


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
def ativo(request, asset_id):
    if not request.user.is_authenticated:
        return redirect('login')

    asset = get_object_or_404(Asset, pk=asset_id)

    get_loan = get_loan_asset(asset_id)

    if get_loan['status']:
        for loan in get_loan['queryset']:
            queryset = loan
        context = {
            'asset': asset,
            'is_loan': True,
            'loan': queryset
        }
    else:
        context = {
            'asset': asset,
            'is_loan': False,
            'loan': None
        }

    return render(request, 'apps/tech_assets/ativo.html', context)


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
def carrinho(request):
    if not request.user.is_authenticated:
        return redirect('login')

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

    # Passe os dados para o template
    context = {
        'page_obj': page_obj,
        'query': query,
    }

    # Redireciona para a lista de itens
    return render(request, 'apps/tech_assets/carrinho_cards.html', context)


@login_required
@group_required(['Suporte'], redirect_url='forbidden_url')
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
@group_required(['Suporte'], redirect_url='forbidden_url')
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
@group_required(['Suporte'], redirect_url='forbidden_url')
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


@login_required
@group_required(['Aprovadores', 'Administradores'], redirect_url='forbidden_url')
def aprovacoes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_instance = get_object_or_404(User, username=request.user)

    # Se houver usuario
    if user_instance:
        try:
            query = request.GET.get('q', '')
            aprovacoes = Approval.objects.all()
            # Query pode ser alterada dependendo de como queremos consultar
            if query:
                aprovacoes = aprovacoes.filter(
                    # Q(aprovador__icontains=query) |
                    Q(status_aprovacao__icontains=query)
                )

            paginator = Paginator(aprovacoes, 15)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'aprovacoes': aprovacoes,
                'url_form': resolve(request.path_info).url_name,
                'page_obj': page_obj,
                'query': query,
            }

            return render(request, 'apps/tech_assets/aprovacoes.html', context)
        except Exception as e:
            print(f'ERROR :: DELETA CARRINHO :: {e}')

    return redirect('index')


@login_required
@group_required(['Administradores', 'Aprovadores'], redirect_url='forbidden_url')
def aprovacao(request):
    if not request.user.is_authenticated:
        return redirect('login')
    pass


@login_required
def forbidden_url(request):
    return render(request, 'shared/forbidden_page.html')


@login_required
def cadastro_ativos_csv(request):
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            upload_assets(csv_file, request.user)

                    
    return render(request, 'apps/tech_assets/upload_csv.html', {'form': form})
