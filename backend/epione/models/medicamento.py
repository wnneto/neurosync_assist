from django.db import models

class Medicamento(models.Model):
    CATEGORIA_CHOICES = [
        ("analgésico", "Analgésico"),
        ("antiinflamatorio", "Anti-inflamatório"),
        ("anticonvulsivante", "Anticonvulsivante"),
        ("neuromodulador", "Neuromodulador"),
        ("antidepressivo", "Antidepressivo"),
        ("ansiolítico", "Ansiolítico"),
        ("outro", "Outro"),
    ]

    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)

    class Meta:
        verbose_name_plural = "Medicamentos"

    def __str__(self):
        return self.nome
