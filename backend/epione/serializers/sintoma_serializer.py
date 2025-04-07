from rest_framework import serializers
from epione.models.sintoma import Sintoma


class SintomaSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField(many=True)

    class Meta:
        model = Sintoma
        fields = ['codigo', 'descricao', 'categoria']
