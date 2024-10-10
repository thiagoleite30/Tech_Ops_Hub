from django.urls import path
from apps.tech_api.api.viewsets import FileUploadViewSet

urlpatterns = [
    path('upload_assets/', FileUploadViewSet.as_view({'post': 'create'}), name='file-upload'),  # Endpoint para upload de arquivos
]