import pandas as pd
from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.tech_api.api.serializers import FileUploadSerializer
from apps.tech_assets.services import upload_assets


class FileUploadViewSet(viewsets.ModelViewSet):
    serializer_class = FileUploadSerializer
    
    def create(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            file = request.FILES.get('file')

            if not file:
                return Response({'error': 'Nenhum arquivo enviado'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                upload_assets(file)
                #df = pd.read_csv(file, sep=';')

                #print(df)

                return Response({"message": "Arquivo CSV processado e enviado com sucesso."}, status=status.HTTP_201_CREATED)

            
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)