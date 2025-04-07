# epione/serializers/medicamento_serializer.py
from rest_framework import serializers
from epione.models.medicamento import Medicamento

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ['id', 'nome', 'descricao', 'categoria']
