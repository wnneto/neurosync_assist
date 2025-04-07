from rest_framework import serializers
from atendimento.models import Atendimento
from atendimento.models.atendimento import Consulta

class AtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        fields = [
            'id', 'consulta', 'relatorio', 'cid',
            'exames_solicitados', 'tratamento_recomendado',
            'link_telemedicina',  # <- Aqui
            'criado_em'
        ]
        read_only_fields = ['id', 'criado_em']



        
class IniciarTelemedicinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = ['id', 'link_telemedicina']