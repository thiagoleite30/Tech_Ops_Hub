from django.urls import path
from apps.move_gpos.views import  request

# Lista de endpoints:
urlpatterns = [
    path('request/', request, name='request')
]
