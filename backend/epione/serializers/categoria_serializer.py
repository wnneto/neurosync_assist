# epione/serializers/categoria_serializer.py
from rest_framework import serializers
from epione.models.categoria import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao']
