from rest_framework import serializers
from fichamedica.models.farmacia import Medicamento



class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ['id', 'nome', 'descricao', 'categoria']