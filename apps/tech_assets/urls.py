from django.urls import include, path
from apps.tech_assets.views import forbidden_url, index, login, cadastro_fabricante, \
    cadastro_centro_custo, cadastro_tipo_ativo, cadastro_local, \
    cadastro_manutencao, cadastro_ativo, ativos, novo_emprestimo, \
    carrinho, add_carrinho, remove_do_carrinho, cadastro_modelo, \
    deleta_carrinho, aprovacoes, aprovacao, ativo, concluir_manutencao, \
    cadastro_ativos_csv

# Lista de endpoints:
urlpatterns = [
    path('', index, name='index'),
    path('login', login, name='login'),
    path('forbidden_url', forbidden_url, name='forbidden_url'),
    path('cadastro_fabricante/', cadastro_fabricante, name='cadastro_fabricante'),
    path('cadastro_modelo/', cadastro_modelo, name='cadastro_modelo'),
    path('cadastro_centro_custo/', cadastro_centro_custo,
         name='cadastro_centro_custo'),
    path('cadastro_tipo_ativo/', cadastro_tipo_ativo, name='cadastro_tipo_ativo'),
    path('cadastro_local/', cadastro_local, name='cadastro_local'),
    path('cadastro_manutencao/<int:asset_id>/',
         cadastro_manutencao, name='cadastro_manutencao'),
    path('concluir_manutencao/<int:asset_id>/',
         concluir_manutencao, name='concluir_manutencao'),
    path('cadastro_ativo/', cadastro_ativo, name='cadastro_ativo'),
    path('ativos/', ativos, name='ativos'),
    path('ativo/<int:asset_id>/', ativo, name='ativo'),
    path('novo_emprestimo/', novo_emprestimo, name='novo_emprestimo'),
    path('carrinho/', carrinho, name='carrinho'),
    path('add_carrinho/<int:asset_id>/', add_carrinho, name='add_carrinho'),
    path('remove_do_carrinho/<int:asset_id>/',
         remove_do_carrinho, name='remove_do_carrinho'),
    path('deleta_carrinho/', deleta_carrinho, name='deleta_carrinho'),
    path('aprovacoes/', aprovacoes, name='aprovacoes'),
    path('aprovacao/', aprovacao, name='aprovacao'),
    path('upload_csv/', cadastro_ativos_csv, name='upload_csv')
]
