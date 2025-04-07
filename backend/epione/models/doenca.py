# epione/models/doenca.py
from django.db import models
from epione.models.sintoma import Sintoma

class Doenca(models.Model):
    cid = models.CharField(max_length=10, unique=True)
    descricao = models.TextField()
    sintomas = models.ManyToManyField(Sintoma, related_name="doencas")

    class Meta:
        verbose_name_plural = "Doenças"

    def __str__(self):
        return f"{self.cid} - {self.descricao[:50]}"
