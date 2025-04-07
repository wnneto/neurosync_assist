# epione/serializers/especialidade_serializer.py
from rest_framework import serializers
from epione.models.especialidade import Especialidade

class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = ['id', 'nome', 'descricao']
