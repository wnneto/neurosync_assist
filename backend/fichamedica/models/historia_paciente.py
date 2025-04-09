# fichamedica/models/dados.py

from django.db import models
from django.conf import settings
from .farmacia import TipoMedicamento
from .fatores import Alergia, DoencaCronica


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


class Cirurgia(models.Model):
    dados_medicos = models.ForeignKey('fichamedica.DadosMedicos', on_delete=models.CASCADE, related_name='cirurgias')
    categoria = models.CharField(max_length=20, choices=[
        ('cardiaca', 'Cardíaca'), ('ortopedica', 'Ortopédica'),
        ('neurologica', 'Neurológica'), ('oftalmologica', 'Oftalmológica'),
        ('ginecologica', 'Ginecológica'), ('digestiva', 'Digestiva'),
        ('respiratoria', 'Respiratória'), ('renal', 'Renal'),
        ('outra', 'Outra'),
    ])
    periodo = models.CharField(max_length=10, choices=[
        ('<6m', 'Menos de 6 meses'), ('6m-1a', '6 meses a 1 ano'),
        ('1-3a', '1 a 3 anos'), ('>3a', 'Mais de 3 anos'), ('dk', 'Desconhecido')
    ])
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_categoria_display()} ({self.get_periodo_display()})"

