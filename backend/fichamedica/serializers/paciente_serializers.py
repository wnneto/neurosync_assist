# fichamedica/serializers/paciente_serializers.py

from rest_framework import serializers
from fichamedica.models import Anamnese, Exame, HistoricoFamiliar
import os


# ========== HISTÓRICO FAMILIAR ==========
class HistoricoFamiliarSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoFamiliar
        fields = ['doenca', 'parentesco']


# ========== ANAMNESE ==========
SINTOMAS_CHOICES = [
    ("febre", "Febre"),
    ("tosse", "Tosse"),
    ("cefaleia", "Cefaleia"),
    ("mialgia", "Dores Musculares"),
    ("fadiga", "Fadiga"),
    ("nausea", "Náusea"),
    ("vomito", "Vômito"),
    ("diarreia", "Diarreia"),
    ("dispneia", "Dificuldade Respiratória"),
    ("dor_abdominal", "Dor Abdominal"),
    ("congestao", "Congestão Nasal"),
    ("perda_olfato", "Perda de Olfato ou Paladar"),
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


# ========== EXAMES ==========
EXTENSOES_PERMITIDAS = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']

class ExameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exame
        fields = ['id', 'tipo', 'periodo', 'arquivo', 'descricao']

    def validate_arquivo(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in EXTENSOES_PERMITIDAS:
            raise serializers.ValidationError(
                "Extensão de arquivo não permitida. Aceitamos apenas: PDF, JPG, PNG, DOC e DOCX."
            )
        return value
