from django.shortcuts import render
from apps.tech_assets.models import Approval
from apps.tech_assets.services import register_logentry
from django.contrib.admin.models import CHANGE, DELETION, ADDITION
from django.shortcuts import get_object_or_404, render, redirect
from apps.tech_assets.forms import AssetAllocationForms, AssetForms, MaintenanceForms, \
    LocationForms, ManufacturerForms, CostCenterForms, \
    AssetTypeForms
from django.urls import resolve

# Create your views here.


def index(request):
    aprovacoes_pendentes = Approval.objects.filter(status_aprovacao='pendente').exists()
    print(f'DEBUG :: VIEW :: INDEX :: {aprovacoes_pendentes}')
    return render(request, 'apps/tech_assets/index.html', {'aprovacoes_pendentes': aprovacoes_pendentes})


def cadastro_fabricante(request):
    """
    if not request.user.is_authenticated:
        print(f'DEBUG :: INDEX :: NÃO TEM USUÁRIO')
        #messages.error(request, "Usuário não autenticado!")
        return redirect('login')"""

    form = ManufacturerForms

    if request.method == 'POST':
        form = ManufacturerForms(request.POST, request.FILES)

        if form.is_valid():
            # register_logentry(instance=form.save(usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')
            form.save()

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_local')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


def cadastro_centro_custo(request):
    """
    if not request.user.is_authenticated:
        print(f'DEBUG :: INDEX :: NÃO TEM USUÁRIO')
        #messages.error(request, "Usuário não autenticado!")
        return redirect('login')"""

    form = CostCenterForms

    if request.method == 'POST':
        form = CostCenterForms(request.POST, request.FILES)

        if form.is_valid():
            # register_logentry(instance=form.save(usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')
            form.save()

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_local')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


def cadastro_tipo_ativo(request):
    """
    if not request.user.is_authenticated:
        print(f'DEBUG :: INDEX :: NÃO TEM USUÁRIO')
        #messages.error(request, "Usuário não autenticado!")
        return redirect('login')"""

    form = AssetTypeForms

    if request.method == 'POST':
        form = AssetTypeForms(request.POST, request.FILES)

        if form.is_valid():
            # register_logentry(instance=form.save(usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')
            form.save()

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_local')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


def cadastro_local(request):
    """
    if not request.user.is_authenticated:
        print(f'DEBUG :: INDEX :: NÃO TEM USUÁRIO')
        #messages.error(request, "Usuário não autenticado!")
        return redirect('login')"""

    form = LocationForms

    if request.method == 'POST':
        form = LocationForms(request.POST, request.FILES)

        if form.is_valid():
            # register_logentry(instance=form.save(usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')
            form.save()

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_local')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


def cadastro_manutencao(request):
    """
    if not request.user.is_authenticated:
        print(f'DEBUG :: INDEX :: NÃO TEM USUÁRIO')
        #messages.error(request, "Usuário não autenticado!")
        return redirect('login')"""

    form = MaintenanceForms

    if request.method == 'POST':
        form = MaintenanceForms(request.POST, request.FILES)

        if form.is_valid():
            # register_logentry(instance=form.save(usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')
            form.save()

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_manutencao')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})


def cadastro_ativo(request):
    """
    if not request.user.is_authenticated:
        print(f'DEBUG :: INDEX :: NÃO TEM USUÁRIO')
        #messages.error(request, "Usuário não autenticado!")
        return redirect('login')"""

    form = AssetForms
    
    print(f'DEBUG :: VIEW :: CADASTRO ATIVO :: {form.form_name}')

    if request.method == 'POST':
        form = AssetForms(request.POST, request.FILES)

        if form.is_valid():
            # register_logentry(instance=form.save(usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')
            form.save()

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('cadastro_ativo')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})

def novo_emprestimo(request):
    """
    if not request.user.is_authenticated:
        print(f'DEBUG :: INDEX :: NÃO TEM USUÁRIO')
        #messages.error(request, "Usuário não autenticado!")
        return redirect('login')"""

    form = AssetAllocationForms
    
    print(f'DEBUG :: VIEW :: CADASTRO ATIVO :: {form.form_name}')

    if request.method == 'POST':
        form = AssetAllocationForms(request.POST, request.FILES)

        if form.is_valid():
            # register_logentry(instance=form.save(usuario=request.user), action=ADDITION, user=request.user)
            # messages.success(request, 'Nova imagem cadastrada na galeria')
            form.save()

            if 'save' in request.POST:
                return redirect('index')
            elif 'save_and_add' in request.POST:
                return redirect('novo_emprestimo')

    return render(request, 'apps/tech_assets/cadastro.html', {'form': form, 'url_form': resolve(request.path_info).url_name})
