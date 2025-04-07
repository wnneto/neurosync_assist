from rest_framework import serializers
from atendimento.models import DocumentoConsulta

class DocumentoConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoConsulta
        fields = ['id', 'atendimento', 'tipo', 'conteudo', 'criado_em']
        read_only_fields = ['id', 'criado_em']
