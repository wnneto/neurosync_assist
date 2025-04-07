# fichamedica/models/dados.py

from django.db import models
from django.conf import settings
from django.forms import ValidationError
from .referencias import Alergia, DoencaCronica, TipoMedicamento


class DadosMedicos(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dados_medicos')
    alergias = models.ManyToManyField(Alergia, blank=True)
    medicamentos_em_uso = models.ManyToManyField(TipoMedicamento, blank=True)
    doencas_cronicas = models.ManyToManyField(DoencaCronica, blank=True)
    observacoes_gerais = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Dados médicos de {self.usuario.nome}"


class HistoricoFamiliar(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='historico_familiar')
    doenca = models.ForeignKey(DoencaCronica, on_delete=models.CASCADE)
    parentesco = models.CharField(max_length=10, choices=[
        ("pai", "Pai"), ("mae", "Mãe"), ("avo", "Avô/Avó"),
        ("irmao", "Irmão/Irmã"), ("filho", "Filho/Filha"), ("outro", "Outro")
    ])

    def __str__(self):
        return f"{self.get_parentesco_display()} com {self.doenca.nome}"


class Anamnese(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='anamnese')
    sintomas = models.JSONField(default=list, help_text="Selecione entre 3 a 5 sintomas.")
    periodo = models.CharField(max_length=20, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not (3 <= len(self.sintomas) <= 5):
            raise ValidationError("Você deve selecionar entre 3 e 5 sintomas.")

    def __str__(self):
        return f"Anamnese de {self.usuario.nome}"
