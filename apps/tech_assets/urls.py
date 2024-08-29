from django.urls import include, path
from apps.tech_assets.views import zona_restrita, index, login, cadastro_fabricante, \
    cadastro_centro_custo, cadastro_tipo_ativo, cadastro_local, \
    cadastro_manutencao, cadastro_ativo, ativos, novo_movimento, \
    carrinho, add_carrinho, remove_do_carrinho, cadastro_modelo, \
    deleta_carrinho, aprovacoes, aprovacao, ativo, concluir_manutencao, \
    cadastro_ativos_csv, aprova_movimentacao, reprova_movimentacao, \
    termos, termo, cadastro_acessorio, get_accessory_options, \
    editar_aprovacao, aceita_termo, recusa_termo, devolucao, \
    get_assets_return_options


# Lista de endpoints:
urlpatterns = [
    path('', index, name='index'),
    path('login', login, name='login'),
    path('zona_restrita', zona_restrita, name='zona_restrita'),
    path('cadastro_fabricante/', cadastro_fabricante, name='cadastro_fabricante'),
    path('cadastro_modelo/', cadastro_modelo, name='cadastro_modelo'),
    path('cadastro_centro_custo/', cadastro_centro_custo,
         name='cadastro_centro_custo'),
    path('cadastro_tipo_ativo/', cadastro_tipo_ativo, name='cadastro_tipo_ativo'),
    path('cadastro_local/', cadastro_local, name='cadastro_local'),
    path('cadastro_manutencao/<int:asset_id>/',
         cadastro_manutencao, name='cadastro_manutencao'),
    path('cadastro_acessorio/', cadastro_acessorio, name='cadastro_acessorio'),
    path('concluir_manutencao/<int:asset_id>/',
         concluir_manutencao, name='concluir_manutencao'),
    path('cadastro_ativo/', cadastro_ativo, name='cadastro_ativo'),
    path('ativos/', ativos, name='ativos'),
    path('ativo/<int:asset_id>/', ativo, name='ativo'),
    path('novo_movimento/', novo_movimento, name='novo_movimento'),
    path('carrinho/', carrinho, name='carrinho'),
    path('add_carrinho/<int:asset_id>/', add_carrinho, name='add_carrinho'),
    path('remove_do_carrinho/<int:asset_id>/',
         remove_do_carrinho, name='remove_do_carrinho'),
    path('deleta_carrinho/', deleta_carrinho, name='deleta_carrinho'),
    path('aprovacoes/', aprovacoes, name='aprovacoes'),
    path('aprovacao/<int:aprovacao_id>/', aprovacao, name='aprovacao'),
    path('editar_aprovacao/<int:aprovacao_id>/',
         editar_aprovacao, name='editar_aprovacao'),
    path('aprova_movimentacao/<int:aprovacao_id>/',
         aprova_movimentacao, name='aprova_movimentacao'),
    path('reprova_movimentacao/<int:aprovacao_id>/',
         reprova_movimentacao, name='reprova_movimentacao'),
    path('termos/', termos, name='termos'),
    path('termo/<int:termo_id>/', termo, name='termo'),
    path('devolucao/<int:termo_id>/', devolucao, name='devolucao'),
    path('aceita_termo/<int:termo_id>/', aceita_termo, name='aceita_termo'),
    path('recusa_termo/<int:termo_id>/', recusa_termo, name='recusa_termo'),
    path('upload_csv/', cadastro_ativos_csv, name='upload_csv'),
    path('get_accessory_options/', get_accessory_options,
         name='get_accessory_options'),
    path('get_assets_return_options/', get_assets_return_options,
         name='get_assets_return_options')
]
