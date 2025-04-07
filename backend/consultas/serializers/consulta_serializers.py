from rest_framework import serializers
from consultas.models import Consulta
from users.models import CustomUser

class ConsultaSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source='paciente.nome', read_only=True)
    medico_nome = serializers.SerializerMethodField()

    class Meta:
        model = Consulta
        fields = '__all__'

    def get_medico_nome(self, obj):
        if obj.medico:
            return obj.medico.nome
        return "Médico indefinido"
