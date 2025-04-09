# fichamedica/models/referencias.py

from django.db import models


class TipoMedicamento(models.Model):
    CATEGORIA_CHOICES = [
        ("analgésico", "Analgésico"),
        ("antiinflamatorio", "Anti-inflamatório"),
        ("anticonvulsivante", "Anticonvulsivante"),
        ("neuromodulador", "Neuromodulador"),
        ("antidepressivo", "Antidepressivo"),
        ("ansiolítico", "Ansiolítico"),
        ('pressao', 'Pressão'),
        ('humor', 'Estabilizante de Humor'),
        ('diabetes', 'Diabetes'),
        ('colesterol', 'Colesterol'),
        ('cardiaco', 'Cardíaco'),
        ('outro', 'Outro'),
    ]

    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)

    class Meta:
        verbose_name_plural = "Medicamentos"

    def __str__(self):
        return self.nome


class Medicamento(models.Model):
    pass



