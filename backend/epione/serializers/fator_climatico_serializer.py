# epione/serializers/fator_climatico_serializer.py
from rest_framework import serializers
from epione.models.fator_climatico import FatorClimatico

class FatorClimaticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatorClimatico
        fields = ['id', 'nome', 'descricao']
