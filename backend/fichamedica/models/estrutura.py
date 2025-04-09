from django.db import models
from django.conf import settings
from django.forms import ValidationError
from .dados_md import Categoria

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
    
class Sintoma(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.CharField(max_length=100)
    categorias = models.ManyToManyField(Categoria, related_name='sintomas')  # 👈 isso aqui é essencial

    class Meta:
        verbose_name_plural = "Sintomas"

    def __str__(self):
        return self.descricao



class Doenca(models.Model):
    cid = models.CharField(max_length=10, unique=True)
    descricao = models.TextField()
    sintomas = models.ManyToManyField(Sintoma, related_name="doencas")

    class Meta:
        verbose_name_plural = "Doenças"

    def __str__(self):
        return f"{self.cid} - {self.descricao[:50]}"


