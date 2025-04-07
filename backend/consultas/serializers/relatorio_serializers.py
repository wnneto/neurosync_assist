from rest_framework import serializers
from consultas.models import RelatorioConsulta

class RelatorioConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatorioConsulta
        fields = [
            "id", "consulta", "introducao_gerada", "descricao_complementar",
            "cid10", "exames_solicitados", "tratamento_orientado",
            "visivel_para_paciente", "criado_em", "atualizado_em"
        ]
        read_only_fields = ["introducao_gerada", "criado_em", "atualizado_em"]
