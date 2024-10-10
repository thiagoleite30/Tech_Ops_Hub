from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


    def validate_file(self, value):
        if value.size > 50*1024*1024:
            raise serializers.ValidationError("O arquivo é muito grande. Ultrapassa o limite de 50MB.")
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("O arquivo deve ser um arquivo CSV.")
        
        return value