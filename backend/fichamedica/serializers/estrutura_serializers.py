from rest_framework import serializers
from fichamedica.models.estrutura import Doenca, Sintoma






class SintomaSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField(many=True)

    class Meta:
        model = Sintoma
        fields = ['codigo', 'descricao', 'categoria']



class DoencaSerializer(serializers.ModelSerializer):
    sintomas = SintomaSerializer(many=True, read_only=True)

    class Meta:
        model = Doenca
        fields = ['id', 'cid', 'descricao', 'sintomas']


    sintomas = serializers.PrimaryKeyRelatedField(
        queryset=Sintoma.objects.all(),
        many=True
    )