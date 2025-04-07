# epione/serializers/doenca_serializer.py
from rest_framework import serializers
from epione.models.doenca import Doenca
from epione.models.sintoma import Sintoma
from epione.serializers.sintoma_serializer import SintomaSerializer

class DoencaSerializer(serializers.ModelSerializer):
    sintomas = SintomaSerializer(many=True, read_only=True)

    class Meta:
        model = Doenca
        fields = ['id', 'cid', 'descricao', 'sintomas']


    sintomas = serializers.PrimaryKeyRelatedField(
        queryset=Sintoma.objects.all(),
        many=True
    )
