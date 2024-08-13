from django.urls import include, path
from apps.tech_assets.views import index, login, cadastro_fabricante, \
    cadastro_centro_custo, cadastro_tipo_ativo, cadastro_local, \
    cadastro_manutencao, cadastro_ativo, ativos, novo_emprestimo, \
    carrinho, add_carrinho, remove_do_carrinho, cadastro_modelo, \
    deleta_carrinho, aprovacoes, aprovacao

# Lista de endpoints:
urlpatterns = [
    path('', index, name='index'),
    path('login', login, name='login'),
    path('cadastro_fabricante/', cadastro_fabricante, name='cadastro_fabricante'),
    path('cadastro_modelo/', cadastro_modelo, name='cadastro_modelo'),
    path('cadastro_centro_custo/', cadastro_centro_custo,
         name='cadastro_centro_custo'),
    path('cadastro_tipo_ativo/', cadastro_tipo_ativo, name='cadastro_tipo_ativo'),
    path('cadastro_local/', cadastro_local, name='cadastro_local'),
    path('cadastro_manutencao/', cadastro_manutencao, name='cadastro_manutencao'),
    path('cadastro_ativo/', cadastro_ativo, name='cadastro_ativo'),
    path('novo_emprestimo/', novo_emprestimo, name='novo_emprestimo'),
    # path("select2/", include("django_select2.urls")),
    path('carrinho/', carrinho, name='carrinho'),
    path('add_carrinho/<int:asset_id>/', add_carrinho, name='add_carrinho'),
    path('remove_do_carrinho/<int:asset_id>/',
         remove_do_carrinho, name='remove_do_carrinho'),
    path('deleta_carrinho/', deleta_carrinho, name='deleta_carrinho'),
    path('ativos/', ativos, name='ativos'),
    path('aprovacoes/', aprovacoes, name='aprovacoes'),
    path('aprovacao/', aprovacao, name='aprovacao'),
]
