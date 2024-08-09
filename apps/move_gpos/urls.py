from django.urls import path
from apps.move_gpos.views import index, request

# Lista de endpoints:
urlpatterns = [
    path('', index),
    path('request/', request, name='request')
]
