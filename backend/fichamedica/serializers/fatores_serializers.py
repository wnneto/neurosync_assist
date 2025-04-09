from rest_framework import serializers
from fichamedica.models.fatores import FatorClimatico



class FatorClimaticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatorClimatico
        fields = ['id', 'nome', 'descricao']