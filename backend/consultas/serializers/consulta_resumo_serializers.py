# consultas/serializers/consulta_resumo.py (novo arquivo, modularizado!)

from rest_framework import serializers
from consultas.models import Consulta

class ConsultaResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = ['id', 'data', 'status', 'tipo', 'comparecimento']  # Adapte conforme necessário
