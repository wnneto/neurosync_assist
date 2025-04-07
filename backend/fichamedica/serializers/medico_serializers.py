from rest_framework import serializers
from fichamedica.models import (
    DadosMedicos, DoencaCronica, Alergia, TipoMedicamento,
    Cirurgia, HistoricoFamiliar, Anamnese, Exame
)
import os

# ======================= CIRURGIAS =========================
class CirurgiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cirurgia
        fields = ['categoria', 'periodo', 'observacao']


# ======================= HISTÓRICO FAMILIAR =========================
class HistoricoFamiliarSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoFamiliar
        fields = ['doenca', 'parentesco']


# ======================= DADOS MÉDICOS =========================
class DadosMedicosSerializer(serializers.ModelSerializer):
    doencas_cronicas = serializers.PrimaryKeyRelatedField(many=True, queryset=DoencaCronica.objects.all())
    alergias = serializers.PrimaryKeyRelatedField(many=True, queryset=Alergia.objects.all())
    medicamentos_em_uso = serializers.PrimaryKeyRelatedField(many=True, queryset=TipoMedicamento.objects.all())
    cirurgias = CirurgiaSerializer(many=True)
    historico_familiar = serializers.SerializerMethodField()

    class Meta:
        model = DadosMedicos
        fields = [
            'doencas_cronicas', 'alergias', 'medicamentos_em_uso',
            'cirurgias', 'historico_familiar', 'observacoes_gerais'
        ]

    def get_historico_familiar(self, obj):
        historico = obj.usuario.historico_familiar.all()
        return HistoricoFamiliarSerializer(historico, many=True).data

    def create(self, validated_data):
        cirurgia_data = validated_data.pop('cirurgias', [])
        historico_data = validated_data.pop('historico_familiar', [])
        dados = DadosMedicos.objects.create(usuario=self.context['request'].user, **validated_data)

        for item in cirurgia_data:
            Cirurgia.objects.create(dados_medicos=dados, **item)

        for item in historico_data:
            HistoricoFamiliar.objects.create(usuario=self.context['request'].user, **item)

        return dados

    def update(self, instance, validated_data):
        cirurgia_data = validated_data.pop('cirurgias', [])
        historico_data = validated_data.pop('historico_familiar', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if cirurgia_data:
            instance.cirurgias.all().delete()
            for item in cirurgia_data:
                Cirurgia.objects.create(dados_medicos=instance, **item)

        if historico_data:
            instance.usuario.historico_familiar.all().delete()
            for item in historico_data:
                HistoricoFamiliar.objects.create(usuario=instance.usuario, **item)

        return instance


# ======================= ANAMNESE =========================
SINTOMAS_CHOICES = [
    ("febre", "Febre"),
    ("tosse", "Tosse"),
    ("cefaleia", "Cefaleia"),
    ("mialgia", "Dores Musculares"),
    ("fadiga", "Fadiga"),
    ("náusea", "Náusea"),
    ("vômito", "Vômito"),
    ("diarreia", "Diarreia"),
    ("dispneia", "Dificuldade Respiratória"),
    ("dor_abdominal", "Dor Abdominal"),
    ("congestao", "Congestão Nasal"),
    ("anorexia", "Falta de Apetite"),
    ("sudorese", "Sudorese Noturna")
]

class AnamneseSerializer(serializers.ModelSerializer):
    sintomas = serializers.ListField(
        child=serializers.ChoiceField(choices=SINTOMAS_CHOICES),
        help_text="Selecione de 3 a 5 sintomas."
    )

    class Meta:
        model = Anamnese
        fields = ['sintomas', 'periodo']

    def validate_sintomas(self, value):
        if not (3 <= len(value) <= 5):
            raise serializers.ValidationError("Você deve selecionar entre 3 e 5 sintomas.")
        return value


# ======================= EXAMES =========================
EXTENSOES_PERMITIDAS = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']

class ExameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exame
        fields = ['id', 'tipo', 'periodo', 'arquivo', 'descricao']

    def validate_arquivo(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in EXTENSOES_PERMITIDAS:
            raise serializers.ValidationError("Extensão de arquivo não permitida. Aceitamos apenas: PDF, JPG, PNG, DOC e DOCX.")
        return value
