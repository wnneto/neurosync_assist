# fichamedica/models/referencias.py

from django.db import models

class DoencaCronica(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Alergia(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class TipoMedicamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Medicamento(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=[
        ('pressao', 'Pressão'),
        ('humor', 'Estabilizante de Humor'),
        ('diabetes', 'Diabetes'),
        ('colesterol', 'Colesterol'),
        ('cardiaco', 'Cardíaco'),
        ('ansiolitico', 'Ansiolítico'),
        ('outro', 'Outro'),
    ])

    def __str__(self):
        return f"{self.nome} ({self.get_categoria_display()})"
