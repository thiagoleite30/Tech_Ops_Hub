import traceback
from django.http import JsonResponse
from django.shortcuts import render
from apps.tech_assets.models import Accessory, Approval, Asset, \
    AssetCart, AssetInfo, AssetModel, AssetType, Cart, CostCenter, \
    Location, Manufacturer, Movement, MovementAccessory, MovementAsset, \
    Maintenance, ReturnTerm, Termo
from django.shortcuts import get_object_or_404, render, redirect

from apps.tech_assets.services import register_logentry, upload_assets, \
    concluir_manutencao_service
from django.contrib.admin.models import ADDITION, CHANGE

from apps.tech_assets.forms import AccessoryForms, ApprovalForms, \
    AssetModelForms, CSVUploadForm, DynamicAccessoryFormSet, \
    MovementForms, AssetForms, MaintenanceForms, \
    LocationForms, ManufacturerForms, CostCenterForms, \
    AssetTypeForms, ReturnTermForms, TermoForms
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Q, Case, \
    When, Value, IntegerField
from django.core.paginator import Paginator
from apps.tech_persons.models import Profile
from utils.decorators import group_required
from django.contrib import messages

# from django.views.decorators.cache import cache_page

# Create your views here.


def login(request):
    return render(request, 'shared/login.html')


@login_required
def zona_restrita(request):
    return render(request, 'shared/zona_restrita.html')


@login_required
@group_required(['Suporte', 'Basico', 'Move GPOS'], redirect_url='zona_restrita')
def index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    # info_perfil = get_profile_info(request)
    perfil, create = Profile.objects.get_or_create(user=request.user)
    perfil.employee_id = request.session['employeeId']

    perfil.save()

    grupos = ['Move GPOS']
    if user.groups.filter(name__in=grupos).exists():
        return redirect('move_gpos')

    return render(request, 'apps/tech_assets/index.html')


@login_required
@group_required(['Suporte'], redirect_url='zona_restrita')
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
@group_required(['Suporte'], redirect_url='zona_restrita')
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
@group_required(['Suporte'], redirect_url='zona_restrita')
def cadastro_acessorio(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = AccessoryForms

    if request.method == 'POST':
        form = AccessoryForms(request.POST, request.FILES)

        if form.is_valid():
            register_logentry(instance=form.save(),
                              action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_acessorio')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


@login_required
@group_required(['Suporte'], redirect_url='zona_restrita')
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
@group_required(['Suporte'], redirect_url='zona_restrita')
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
@group_required(['Suporte'], redirect_url='zona_restrita')
# @group_required('Admin', redirect_url='zona_restrita')
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
@group_required(['Suporte'], redirect_url='zona_restrita')
def cadastro_manutencao(request, asset_id):
    if not request.user.is_authenticated:
        return redirect('login')

    form = MaintenanceForms(ativo=asset_id)

    asset = get_object_or_404(Asset, id=asset_id)
    if asset:
        if Maintenance.objects.filter(ativo_id=asset_id, status=True).exists():
            messages.warning(
                request, 'Já existe uma manutenção em aberto para este ativo.')
            url = reverse('ativo', args=[asset_id])
            return redirect(url)

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
@group_required(['Suporte'], redirect_url='zona_restrita')
def concluir_manutencao(request, asset_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if concluir_manutencao_service(asset_id, request.user):
        return redirect('ativo', asset_id=asset_id)
    return redirect('ativos')


@login_required
@group_required(['Suporte'], redirect_url='zona_restrita')
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
@group_required(['Suporte'], redirect_url='zona_restrita')
def get_accessory_options(request):
    options = list(Accessory.objects.all().values('id'))
    for option in options:
        # Adiciona o valor retornado por __str__ para cada item
        accessory = Accessory.objects.get(id=option['id'])
        option['str'] = str(accessory)
    return JsonResponse(options, safe=False)


@login_required
@group_required(['Suporte'], redirect_url='zona_restrita')
def novo_movimento(request):
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

    # Inicialize os formulários
    form = MovementForms(ativos=assets, formset=DynamicAccessoryFormSet)

    if request.method == 'POST':
        form = MovementForms(request.POST, request.FILES, ativos=assets,
                             formset=DynamicAccessoryFormSet(request.POST))

        if form.is_valid():
            print(request.POST.getlist('form-acessorio'))
            print(request.POST.getlist('form-quantidade'))
            movimento = form.save()

            register_logentry(instance=movimento,
                              action=ADDITION, user=request.user)
            deleta_carrinho(request)

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('carrinho')

    return render(request, 'apps/tech_assets/cadastro.html', {
        'form': form,
        'accessory_formset': None,
        'url_form': resolve(request.path_info).url_name,
        'texto': 'Cancelar'
    })


@login_required
@group_required(['Suporte'], redirect_url='zona_restrita')
# @cache_page(60 * 15) # 15 minutos de cache
def ativos(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Defina a query inicial com select_related \
        # Otimizando as consultas
    assets = Asset.objects.select_related('tipo').all()

    # Filtrar os ativos que não estão disponíveis em estoque
    assets_unavailable = assets.exclude(
        status__in=['em_estoque']).values_list('id', flat=True)

    # Subquery para ativos que já estão em carrinho
    subquery = AssetCart.objects.filter(ativo_id=OuterRef('pk')).values('pk')
    assets_in_cart = assets.filter(
        Exists(subquery)).values_list('id', flat=True)

    # Captura a query da URL valores após o q =
    query = request.GET.get('q', '')

    # Criando mapeamento de status pré definidos
    STATUS_MAP = dict((v, k) for k, v in Asset.STATUS_CHOICES)

    # Se houver uma query de busca, aplique filtros
    if query:
        # Procurar status entre os mapeados
        status_codigo = next((codigo for status_legivel, codigo in STATUS_MAP.items(
        ) if query.lower() in status_legivel.lower()), None)
        assets = assets.filter(
            Q(nome__icontains=query) |
            Q(patrimonio__icontains=query) |
            Q(numero_serie__icontains=query) |
            Q(status__icontains=status_codigo if status_codigo else query) |
            Q(tipo__nome__icontains=query)
        )

    # Paginação
    paginator = Paginator(assets.order_by('id'), 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'assets_in_cart': list(assets_in_cart),
        'page_obj': page_obj,
        'query': query,
        'assets_unavailable': list(assets_unavailable),
    }
    return render(request, 'apps/tech_assets/ativos.html', context)


@login_required
@group_required(['Suporte'], redirect_url='zona_restrita')
def ativo(request, asset_id):
    if not request.user.is_authenticated:
        return redirect('login')

    asset = get_object_or_404(Asset, pk=asset_id)
    asset_infos = AssetInfo.objects.get(ativo=asset)
    maintenances = Maintenance.objects.filter(
        ativo_id=asset_id).select_related('ativo')

    if maintenances:
        for maintenance in maintenances:
            Maintenance.dias_de_atraso(maintenance)

    movement = Movement.objects.filter(ativos=asset)

    paginator_movement = Paginator(movement, 10)
    paginator_maintenances = Paginator(maintenances, 10)
    page_number = request.GET.get('page')
    page_obj_movements = paginator_movement.get_page(page_number)
    page_obj_maintenances = paginator_maintenances.get_page(page_number)

    context = {
        'asset': asset,
        'asset_infos': asset_infos if asset_infos else None,
        'maintenances':  maintenances if maintenances else None,
        'is_loan': Movement.objects.filter(ativos=asset).exists(),
        'page_obj_movements': page_obj_movements,
        'page_obj_maintenances': page_obj_maintenances
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'apps/tech_assets/partials/_ativo_tab_content.html', context)

    return render(request, 'apps/tech_assets/ativo.html', context)


@login_required
@group_required(['Suporte'], redirect_url='zona_restrita')
def carrinho(request):

    user_instance = request.user
    if not user_instance.is_authenticated:
        return redirect('login')

    query = request.GET.get('q', '')

    # Obtenha o carrinho do usuário logado
    cart = get_object_or_404(Cart, usuario_sessao=user_instance)

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

    paginator = Paginator(assets, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Passe os dados para o template
    context = {
        'page_obj': page_obj,
        'query': query,
    }

    # Redireciona para a lista de itens
    return render(request, 'apps/tech_assets/carrinho.html', context)


@login_required
@group_required(['Suporte'], redirect_url='zona_restrita')
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
@group_required(['Suporte'], redirect_url='zona_restrita')
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
@group_required(['Suporte'], redirect_url='zona_restrita')
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
@group_required(['Aprovadores TI', 'Administradores', 'Suporte'], redirect_url='zona_restrita')
def aprovacoes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_instance = get_object_or_404(User, username=request.user)

    # Se houver usuario
    if user_instance:
        try:
            query = request.GET.get('q', '')
            aprovacoes = Approval.objects.select_related('movimentacao').all()
            default_status = ['pendente']
            status_aprovacao = request.GET.getlist('status')

            # Query pode ser alterada dependendo de como queremos consultar
            if query:
                aprovacoes = aprovacoes.filter(
                    Q(aprovador__icontains=query) |
                    Q(status_aprovacao__icontains=query) |
                    Q(movimentacao__id__icontains=query) |
                    Q(movimentacao__tipo__icontains=query) |
                    Q(movimentacao__usuario__username__icontains=query) |
                    Q(movimentacao__usuario__first_name__icontains=query) |
                    Q(movimentacao__usuario__last_name__icontains=query)
                )

            status_query = Q()
            if status_aprovacao:

                if 'aprovado' in status_aprovacao:
                    status_query |= Q(status_aprovacao='aprovado')
                if 'reprovado' in status_aprovacao:
                    status_query |= Q(status_aprovacao='reprovado')
                if 'pendente' in status_aprovacao:
                    status_query |= Q(status_aprovacao='pendente')

            # Ordenar por status_aprovacao com 'pendente' primeiro
            aprovacoes = aprovacoes.order_by(
                Case(
                    When(status_aprovacao='pendente', then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                ),
                'status_aprovacao'
            )

            paginator = Paginator(aprovacoes, 16)
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
            print(f'ERROR :: APROVACOES :: {e}')

    return redirect('index')


@login_required
@group_required(['Administradores', 'Aprovadores TI'], redirect_url='zona_restrita')
def aprovacao(request, aprovacao_id):
    if not request.user.is_authenticated:
        return redirect('login')

    aprovacao = get_object_or_404(Approval, pk=aprovacao_id)

    if aprovacao:
        movimentacao = get_object_or_404(
            Movement, pk=aprovacao.movimentacao.id)
        if MovementAsset.objects.filter(movimento=aprovacao.movimentacao).exists():
            ativos_id = [ativo.ativo_id for ativo in MovementAsset.objects.filter(
                movimento=aprovacao.movimentacao)]
            if ativos_id:
                ativos_na_movimentacao = Asset.objects.filter(id__in=ativos_id)
        else:
            ativos_na_movimentacao = []

    if MovementAccessory.objects.filter(movimento=aprovacao.movimentacao).exists():
        acessorios_id = [acessorio.acessorio_id for acessorio in MovementAccessory.objects.filter(
            movimento=aprovacao.movimentacao)]
        if acessorios_id:
            acessorios_na_movimentacao = Accessory.objects.filter(
                id__in=acessorios_id)
            # Criar uma lista de tuplas contendo o acessório e a quantidade
            # Fica assim (acessorio instance, quantidade)
            acessorios_com_quantidade = [
                (acessorio, MovementAccessory.objects.get(
                    movimento=aprovacao.movimentacao, acessorio=acessorio).quantidade)
                for acessorio in acessorios_na_movimentacao
            ]
    else:
        acessorios_com_quantidade = []

    context = {
        'approval': aprovacao,
        'movement': movimentacao if movimentacao else None,
        'assets': ativos_na_movimentacao,
        'accessorys': acessorios_com_quantidade,
    }

    return render(request, 'apps/tech_assets/aprovacao.html', context)


@login_required
@group_required(['Suporte', 'Administradores', 'Aprovadores TI'], redirect_url='zona_restrita')
def editar_aprovacao(request, aprovacao_id):
    if not request.user.is_authenticated:
        return redirect('login')

    aprovacao = get_object_or_404(Approval, pk=aprovacao_id)

    if aprovacao.status_aprovacao != 'pendente':
        messages.warning(
            request, 'Somente aprovações "Pendentes" podem ser alteradas')
        url = reverse('aprovacao', kwargs={'aprovacao_id': aprovacao_id})
        return redirect(url)

    if aprovacao:
        form = ApprovalForms(instance=aprovacao)

        if request.method == 'POST':
            form = ApprovalForms(
                request.POST, request.FILES, instance=aprovacao)

            if form.is_valid():
                register_logentry(instance=form.save(), action=CHANGE,
                                  user=request.user, modificacao='Editada Aprovação')
                messages.success(request, 'Aprovação modificada com sucesso.')
                url = reverse('aprovacao', kwargs={
                              'aprovacao_id': aprovacao_id})
                return redirect(url)

    context = {
        'form': form,
        'id': aprovacao,
        'url_form': resolve(request.path_info).url_name
    }

    return render(request, 'apps/tech_assets/editar.html', context)


@login_required
@group_required(['Aprovadores TI'], redirect_url='zona_restrita')
def aprova_movimentacao(request, aprovacao_id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        # Pega da tabela asset o ativo pelo id
        aprovacao = get_object_or_404(Approval, id=aprovacao_id)
        if aprovacao:
            url = reverse('aprovacao', kwargs={'aprovacao_id': aprovacao_id})
            if aprovacao.status_aprovacao != 'pendente':
                messages.warning(request, f'''Esta aprovação já foi respondida pelo aprovador {
                                 aprovacao.aprovador.username}''')
                return redirect(url)
            if request.user != aprovacao.aprovador:
                messages.warning(
                    request, '''Você não é o aprovador designado para esta movimentação.''')
                return redirect(url)

            Approval.aprovar_movimentacao(aprovacao)
    except Exception as e:
        print(f'ERROR :: APROVA MOVIMENTACAO :: {e}')

    return redirect('aprovacoes')


@login_required
@group_required(['Aprovadores TI'], redirect_url='zona_restrita')
def reprova_movimentacao(request, aprovacao_id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        url = reverse('aprovacao', kwargs={'aprovacao_id': aprovacao_id})
        # Pega da tabela asset o ativo pelo id
        aprovacao = get_object_or_404(Approval, id=aprovacao_id)
        if aprovacao:
            if aprovacao.status_aprovacao != 'pendente':
                messages.warning(request, f'''Esta aprovação já foi respondida pelo aprovador {
                                 aprovacao.aprovador.username}''')
                return redirect(url)
            if request.user != aprovacao.aprovador:
                messages.warning(
                    request, '''Você não é o aprovador designado para esta movimentação.''')
                return redirect(url)

            Approval.reprovar_movimentacao(aprovacao)

    except Exception as e:
        print(f'ERROR :: REPROVA MOVIMENTACAO :: {e}')

    return redirect('aprovacoes')


@login_required
@group_required(['Administradores', 'Suporte', 'TH'], redirect_url='zona_restrita')
def termos(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_instance = get_object_or_404(User, username=request.user)
    # Se houver usuario
    if user_instance:
        try:
            query = request.GET.get('q', '')
            termos = Termo.objects.select_related(
                'movimentacao', 'aprovacao').all()
            status_termos = request.GET.getlist('status')

            # Query pode ser alterada dependendo de como queremos consultar
            if query:
                termos = termos.filter(
                    Q(movimentacao__id__icontains=query) |
                    Q(movimentacao__tipo__icontains=query) |
                    Q(movimentacao__usuario__username__icontains=query) |
                    Q(movimentacao__usuario__first_name__icontains=query) |
                    Q(movimentacao__usuario__last_name__icontains=query) |
                    Q(movimentacao__usuario__profile__employee_id__icontains=query)
                )

            status_query = Q()
            if status_termos:

                if 'aceito' in status_termos:
                    status_query |= Q(aceite_usuario='aceito')
                if 'recusado' in status_termos:
                    status_query |= Q(aceite_usuario='recusado')
                if 'pendente' in status_termos:
                    status_query |= Q(aceite_usuario='pendente')

            termos = termos.filter(status_query).order_by(
                Case(
                    When(aceite_usuario='pendente', then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                ),
                'aceite_usuario'
            )

            paginator = Paginator(termos, 15)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'termos': termos,
                'url_form': resolve(request.path_info).url_name,
                'page_obj': page_obj,
                'query': query,
            }

            return render(request, 'apps/tech_assets/termos.html', context)
        except Exception as e:
            print(f'ERROR :: TERMOS :: {e}')
            traceback.print_exc()

    return redirect('index')


@login_required
@group_required(['Administradores', 'Suporte', 'TH', 'Basico'], redirect_url='zona_restrita')
def termo(request, termo_id):
    if not request.user.is_authenticated:
        return redirect('login')

    term_res = get_object_or_404(Termo, pk=termo_id)
    aprovacao = get_object_or_404(Approval, id=term_res.aprovacao_id)
    movimentacao = get_object_or_404(Movement, pk=aprovacao.movimentacao.id)
    form = TermoForms(instance=term_res)

    if aprovacao:
        ativos_na_movimentacao = list(Asset.objects.filter(
            id__in=MovementAsset.objects.filter(
                movimento=aprovacao.movimentacao).values_list('ativo_id', flat=True)
        ))
        # Caso não haja nenhum ativo atrelado a aprovação então ficará como uma lista vazia
        # Pode ocorrer em casos de movimentações somente de itens classificados como acessórios
        if not ativos_na_movimentacao:
            ativos_na_movimentacao = []

    movements_accessory = list(MovementAccessory.objects.filter(
        movimento=aprovacao.movimentacao).select_related('acessorio'))
    if movements_accessory:
        acessorios_com_quantidade = [
            (movement_acessorio.acessorio, movement_acessorio.quantidade)
            for movement_acessorio in movements_accessory
        ]
    else:
        acessorios_com_quantidade = []

    if request.method == 'POST':
        if term_res.movimentacao.usuario != request.user:
            messages.warning(
                request, 'Você não é o usuário responsável por este termo.')
            url = reverse('termo', args=[termo_id])
            return redirect(url)

        form = TermoForms(request.POST, request.FILES, instance=term_res)
        if form.is_valid():
            term_res.justificativa = form.cleaned_data.get('justificativa')
            term_res.save()
            url = reverse('recusa_termo', args=[termo_id])
            return redirect(url)
        else:
            print(f'Formulário inválido')

    context = {
        'form': form,
        'term': term_res,
        'aprovall': aprovacao,
        'movement': movimentacao if movimentacao else None,
        'assets': ativos_na_movimentacao,
        'accessorys': acessorios_com_quantidade,
        'ReturnTerm': ReturnTerm.objects.filter(movimentacao=movimentacao).exists()
    }

    return render(request, 'apps/tech_assets/termo.html', context)


@login_required
@group_required(['Administradores', 'Aprovadores TI'], redirect_url='zona_restrita')
def aceita_termo(request, termo_id):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        term_res = get_object_or_404(Termo, pk=termo_id)
        url = reverse('termo', kwargs={'termo_id': termo_id})
        if term_res:
            if term_res.status_resposta != False:
                messages.warning(request, 'Este termo já foi respondido.')
                return redirect(url)

            # Busca a movimentação ligada ao termo/fluxo
            movimentacao = get_object_or_404(
                Movement, pk=term_res.movimentacao.id)

            if movimentacao:
                if request.user != movimentacao.usuario:
                    messages.warning(
                        request, 'Você não é o usuário responsável por este termo.')
                    return redirect(url)
                # Método abaixo já faz tudo que é preciso após o aceito \
                    # como mudança de status de ativos, termos e etc...
                term_res.marcar_como_aceito(movimentacao)
                messages.success(request, f'Termo aceito com sucesso!')
                register_logentry(instance=term_res, action=CHANGE,
                                  user=request.user, modificacao='Aceitou os Termos')
    except Exception as e:
        print(f'ERROR :: VIEW :: ACEITA TERMO :: {e}')

    return redirect(url)


@login_required
@group_required(['Administradores', 'Aprovadores TI'], redirect_url='zona_restrita')
def recusa_termo(request, termo_id):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        term_res = get_object_or_404(Termo, pk=termo_id)
        url = reverse('termo', kwargs={'termo_id': termo_id})
        if term_res:
            if term_res.status_resposta != False:
                messages.warning(request, 'Este termo já foi respondido.')
                return redirect(url)

            # Busca a movimentação ligada ao termo/fluxo
            movimentacao = get_object_or_404(
                Movement, pk=term_res.movimentacao.id)
            print(f'DEBUG :: VIEW :: RECUSA TERMO :: {movimentacao}')
            if movimentacao:
                if request.user != movimentacao.usuario:
                    messages.warning(
                        request, 'Você não é o usuário referido neste termo.')
                    return redirect(url)
                # Método abaixo já faz tudo que é preciso após o aceito \
                    # como mudança de status de ativos, termos e etc...
                term_res.marcar_como_recusa(movimentacao)
                messages.success(request, f'Termo recusado com sucesso!')
                register_logentry(instance=term_res, action=CHANGE,
                                  user=request.user, modificacao='Recusou os Termos')
    except Exception as e:
        print(f'ERROR :: VIEW :: RECUSA TERMO :: {e}')
        traceback.print_exc()

    return redirect(url)


@login_required
@group_required(['Suporte'], redirect_url='zona_restrita')
def get_assets_return_options(request):
    options = list(MovementAsset.objects.all().values('id'))
    for option in options:
        # Adiciona o valor retornado por __str__ para cada item
        accessory = MovementAsset.objects.get(id=option['id'])
        option['str'] = str(accessory)
    return JsonResponse(options, safe=False)


@login_required
@group_required(['Administradores', 'Suporte', 'TH'], redirect_url='zona_restrita')
def devolucao(request, termo_id):
    if not request.user.is_authenticated:
        return redirect('login')

    termo = get_object_or_404(Termo, pk=termo_id)
    movimentacao = get_object_or_404(Movement, pk=termo.movimentacao_id)
    url = reverse('termo', kwargs={'termo_id': termo_id})

    if not termo.status_resposta:
        messages.warning(
            request, 'Termo de aceite pendente de resposta do usuário recebedor.')
        return redirect(url)

    if termo.aceite_usuario == 'recusado':
        messages.warning(
            request, 'Este termo não é mais valido.\n Motivo: Recusado pelo usuário.')
        return redirect(url)

    if ReturnTerm.objects.filter(movimentacao=movimentacao).exists():
        messages.warning(request, 'Devolução já registrada anteriormente.')
        return redirect(url)

    accessory_queryset = MovementAccessory.objects.filter(
        movimento=movimentacao)
    movement_assets = MovementAsset.objects.filter(
        movimento=movimentacao, devolvido=False)
    form = ReturnTermForms()

    if request.method == 'POST':
        form = ReturnTermForms(request.POST)

        selected_assets = request.POST.getlist('assets')

        # Convertendo os IDs para instâncias de MovementAsset
        movement_assets = MovementAsset.objects.filter(id__in=selected_assets)

        movement_accessory_ids = request.POST.getlist('movement_accessory_ids')
        quantities = {}
        for movement_accessory_id in movement_accessory_ids:
            quantity = request.POST.get(f'quantities_{movement_accessory_id}')
            if quantity:
                quantities[movement_accessory_id] = int(quantity)

        if form.is_valid():
            # Salvar o termo de devolução
            instance, created = ReturnTerm.objects.get_or_create(
                movimentacao=movimentacao)
            instance.usuario_recebedor = request.user
            instance.observacao = form.cleaned_data.get('observacao', None)
            if created:
                instance.save(usuario=request.user)
            else:
                instance.save()

            for movement_asset in movement_assets:
                movement_asset.marcar_como_devolvido()

            for movement_accessory_id, quantity in quantities.items():
                moviment_accessory = MovementAccessory.objects.get(
                    id=movement_accessory_id)
                moviment_accessory.soma_quantidade_devolvida(quantity)

            register_logentry(instance=instance, action=ADDITION,
                              user=request.user, detalhe='Devolução Inserida')

            messages.success(request, 'Devolução inserida com sucesso.')

            return redirect(url)

    context = {
        'form': form,
        'id': termo_id,
        'movement': movimentacao,
        'url_form': resolve(request.path_info).url_name,
        'accessorys': accessory_queryset,
        'movement_assets': movement_assets,
    }

    return render(request, 'apps/tech_assets/devolucao.html', context)


@login_required
@group_required(['Administradores'], redirect_url='zona_restrita')
def cadastro_ativos_csv(request):
    if not request.user.is_authenticated:
        return redirect('login')
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            upload_assets(csv_file, request.user)

    context = {
        'form': form,
        'url_form': resolve(request.path_info).url_name
    }

    return render(request, 'apps/tech_assets/cadastro.html', context)


@login_required
@group_required(['Administradores', 'Suporte'], redirect_url='zona_restrita')
def acessorios(request):
    if not request.user.is_authenticated:
        return redirect('login')

    acessorios = Accessory.objects.select_related('fabricante').all()

    query = request.GET.get('q', '')
    if query:
        acessorios = acessorios.filter(
            Q(nome__icontains=query) |
            Q(modelo__icontains=query) |
            Q(tipo__icontains=query) |
            Q(fabricante__nome__icontains=query)
        )

    acessorios_lista = acessorios.order_by('id')

    paginator = Paginator(acessorios_lista, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'apps/tech_assets/acessorios.html', context)


@login_required
@group_required(['Administradores', 'Suporte'], redirect_url='zona_restrita')
def editar_acessorio(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    acessorio = get_object_or_404(Accessory, pk=id)
    form = AccessoryForms(instance=acessorio)
    if acessorio:
        if request.method == 'POST':
            form = AccessoryForms(
                request.POST, request.FILES, instance=acessorio)

            if form.is_valid():
                register_logentry(instance=form.save(), action=CHANGE,
                                  user=request.user, modificacao='Editado Acessório')
                messages.success(request, 'Acessório Salvo')

                return redirect('acessorios')

    context = {
        'form': form,
        'id': id,
        'url_form': resolve(request.path_info).url_name
    }

    return render(request, 'apps/tech_assets/editar.html', context)


@login_required
@group_required(['Administradores', 'Suporte'], redirect_url='zona_restrita')
def fabricantes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    fabricantes = Manufacturer.objects.all()

    query = request.GET.get('q', '')
    if query:
        fabricantes = fabricantes.filter(
            Q(nome__icontains=query) |
            Q(telefone__icontains=query) |
            Q(email__icontains=query)
        )

    fabricantes_lista = fabricantes.order_by('id')

    paginator = Paginator(fabricantes_lista, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'apps/tech_assets/fabricantes.html', context)


@login_required
@group_required(['Administradores', 'Suporte'], redirect_url='zona_restrita')
def editar_fabricante(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    fabricante = get_object_or_404(Manufacturer, pk=id)
    form = ManufacturerForms(instance=fabricante)
    if fabricante:
        if request.method == 'POST':
            form = ManufacturerForms(
                request.POST, request.FILES, instance=fabricante)

            if form.is_valid():
                register_logentry(instance=form.save(), action=CHANGE,
                                  user=request.user, modificacao='Editado Registro do Fabricante')
                messages.success(request, 'Fabricante Salvo')

                return redirect('fabricantes')

    context = {
        'form': form,
        'id': id,
        'url_form': resolve(request.path_info).url_name
    }

    return render(request, 'apps/tech_assets/editar.html', context)


@login_required
@group_required(['Administradores', 'Suporte'], redirect_url='zona_restrita')
def centros_custo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cc = CostCenter.objects.all()

    query = request.GET.get('q', '')
    if query:
        cc = cc.filter(
            Q(nome__icontains=query) |
            Q(modelo__icontains=query) |
            Q(tipo__icontains=query) |
            Q(fabricante__nome__icontains=query)
        )

    cc_lista = cc.order_by('id')

    paginator = Paginator(cc_lista, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'apps/tech_assets/centros_custo.html', context)


@login_required
@group_required(['Administradores', 'Suporte'], redirect_url='zona_restrita')
def editar_centro_custo(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    cc = get_object_or_404(CostCenter, pk=id)
    form = CostCenterForms(instance=cc)
    if cc:
        if request.method == 'POST':
            form = AccessoryForms(request.POST, request.FILES, instance=cc)

            if form.is_valid():
                register_logentry(instance=form.save(), action=CHANGE,
                                  user=request.user, modificacao='Editado Registro de Centro de Custo')
                messages.success(request, 'Centro de Custo Salvo')

                return redirect('centros_custo')

    context = {
        'form': form,
        'id': id,
        'url_form': resolve(request.path_info).url_name
    }

    return render(request, 'apps/tech_assets/editar.html', context)


@login_required
@group_required(['Administradores', 'Suporte'], redirect_url='zona_restrita')
def locais(request):
    if not request.user.is_authenticated:
        return redirect('login')

    objetos = Location.objects.all().prefetch_related('local_pai')

    query = request.GET.get('q', '')
    if query:
        objetos = objetos.filter(
            Q(nome__icontains=query) |
            Q(local_pai__nome__icontains=query)
        )

    objetos_lista = objetos.order_by('id')

    paginator = Paginator(objetos_lista, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'apps/tech_assets/locais.html', context)


@login_required
@group_required(['Administradores', 'Suporte'], redirect_url='zona_restrita')
def editar_local(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    objeto = get_object_or_404(Location, pk=id)
    form = LocationForms(instance=objeto)
    if objeto:
        if request.method == 'POST':
            form = LocationForms(request.POST, request.FILES, instance=objeto)

            if form.is_valid():
                register_logentry(instance=form.save(), action=CHANGE,
                                  user=request.user, modificacao='Editado Registro de Local')
                messages.success(request, 'Fabricante Salvo')

                return redirect('fabricantes')

    context = {
        'form': form,
        'id': id,
        'url_form': resolve(request.path_info).url_name
    }

    return render(request, 'apps/tech_assets/editar.html', context)


@login_required
@group_required(['Administradores', 'Suporte'], redirect_url='zona_restrita')
def modelos_ativo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    objetos = AssetModel.objects.select_related('tipo', 'fabricante').all()

    query = request.GET.get('q', '')
    if query:
        objetos = objetos.filter(
            Q(nome__icontains=query) |
            Q(descricao__icontains=query) |
            Q(tipo__nome__icontains=query) |
            Q(fabricante__nome__icontains=query)
        )

    objetos_lista = objetos.order_by('id')

    paginator = Paginator(objetos_lista, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'apps/tech_assets/modelos_ativo.html', context)


@login_required
@group_required(['Administradores', 'Suporte'], redirect_url='zona_restrita')
def editar_modelo(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    objeto = get_object_or_404(AssetModel, pk=id)
    form = AssetModelForms(instance=objeto)
    if objeto:
        if request.method == 'POST':
            form = AssetModelForms(
                request.POST, request.FILES, instance=objeto)

            if form.is_valid():
                register_logentry(instance=form.save(), action=CHANGE,
                                  user=request.user, modificacao='Editado Registro de Modelo de Ativo')
                messages.success(request, 'Modelo de Ativo Salvo')

                return redirect('modelos_ativo')

    context = {
        'form': form,
        'id': id,
        'url_form': resolve(request.path_info).url_name
    }

    return render(request, 'apps/tech_assets/editar.html', context)


@login_required
@group_required(['Administradores', 'Suporte'], redirect_url='zona_restrita')
def tipos_ativo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    objetos = AssetType.objects.all()

    query = request.GET.get('q', '')
    if query:
        objetos = objetos.filter(
            Q(nome__icontains=query) |
            Q(descricao__icontains=query) |
            Q(tipo__nome__icontains=query) |
            Q(fabricante__nome__icontains=query)
        )

    objetos_lista = objetos.order_by('id')

    paginator = Paginator(objetos_lista, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'apps/tech_assets/tipos_ativo.html', context)


@login_required
@group_required(['Administradores', 'Suporte'], redirect_url='zona_restrita')
def editar_tipo_ativo(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    objeto = get_object_or_404(AssetType, pk=id)
    form = AssetTypeForms(instance=objeto)
    if objeto:
        if request.method == 'POST':
            form = AssetTypeForms(request.POST, request.FILES, instance=objeto)

            if form.is_valid():
                register_logentry(instance=form.save(), action=CHANGE,
                                  user=request.user, modificacao='Editado Registro de Tipo de Ativo')
                messages.success(request, 'Tipo de Ativo Salvo')

                return redirect('tipos_ativo')

    context = {
        'form': form,
        'id': id,
        'url_form': resolve(request.path_info).url_name
    }

    return render(request, 'apps/tech_assets/editar.html', context)


@login_required
# @group_required(['Basico'], redirect_url='zona_restrita')
def minhas_movimentacoes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_instance = get_object_or_404(User, username=request.user)
    # Se houver usuario
    if user_instance:
        try:
            query = request.GET.get('q', '')

            termos = Termo.objects.select_related(
                'movimentacao', 'aprovacao').filter(movimentacao__usuario=user_instance)
            status_termos = request.GET.getlist('status')

            # Query pode ser alterada dependendo de como queremos consultar
            if query:
                termos = termos.filter(
                    Q(movimentacao__id__icontains=query) |
                    Q(movimentacao__tipo__icontains=query) |
                    Q(movimentacao__usuario__username__icontains=query) |
                    Q(movimentacao__usuario__first_name__icontains=query) |
                    Q(movimentacao__usuario__last_name__icontains=query)
                )

            status_query = Q()
            if status_termos:

                if 'aceito' in status_termos:
                    status_query |= Q(aceite_usuario='aceito')
                if 'recusado' in status_termos:
                    status_query |= Q(aceite_usuario='recusado')
                if 'pendente' in status_termos:
                    status_query |= Q(aceite_usuario='pendente')

            termos = termos.filter(status_query).order_by(
                Case(
                    When(aceite_usuario='pendente', then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                ),
                'aceite_usuario'
            )

            paginator = Paginator(termos, 15)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'termos': termos,
                'url_form': resolve(request.path_info).url_name,
                'page_obj': page_obj,
                'query': query,
            }

            return render(request, 'apps/tech_assets/termos.html', context)
        except Exception as e:
            print(f'ERROR :: TERMOS :: {e}')

    return redirect('index')
