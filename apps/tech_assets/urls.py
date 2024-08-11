from django.urls import path
from apps.tech_assets.views import index, cadastro_fabricante, \
    cadastro_centro_custo, cadastro_tipo_ativo, cadastro_local, \
    cadastro_manutencao, cadastro_ativo, novo_emprestimo

# Lista de endpoints:
urlpatterns = [
    path('', index, name='index'),
    path('cadastro_fabricante/', cadastro_fabricante, name='cadastro_fabricante'),
    path('cadastro_centro_custo/', cadastro_centro_custo,
         name='cadastro_centro_custo'),
    path('cadastro_tipo_ativo/', cadastro_tipo_ativo, name='cadastro_tipo_ativo'),
    path('cadastro_local/', cadastro_local, name='cadastro_local'),
    path('cadastro_manutencao/', cadastro_manutencao, name='cadastro_manutencao'),
    path('cadastro_ativo/', cadastro_ativo, name='cadastro_ativo'),
    path('novo_emprestimo/',novo_emprestimo,name='novo_emprestimo')
]
