from django.db import models
from .categoria import Categoria

class Sintoma(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.CharField(max_length=100)
    categorias = models.ManyToManyField(Categoria, related_name='sintomas')  # 👈 isso aqui é essencial

    class Meta:
        verbose_name_plural = "Sintomas"

    def __str__(self):
        return self.descricao
