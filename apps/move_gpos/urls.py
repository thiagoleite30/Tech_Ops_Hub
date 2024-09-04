from django.urls import path
from apps.move_gpos.views import  move_gpos, requisicao_troca, get_pdvs, get_gpos

# Lista de endpoints:
urlpatterns = [
    path('move_gpos/', move_gpos, name='move_gpos'),
    path('requisicao_troca/', requisicao_troca, name='requisicao_troca'),
    path('get_pdvs/', get_pdvs, name='get_pdvs'),
    path('get_gpos/', get_gpos, name='get_gpos'),
]
