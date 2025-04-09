from django.db import models
from django.conf import settings


def exame_upload_path(instance, filename):
    return f"exames/{instance.usuario.id}/{filename}"

class Exame(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exames")
    tipo = models.CharField(max_length=20, choices=[
        ("sangue", "Exame de Sangue"), ("urina", "Exame de Urina"),
        ("fezes", "Exame de Fezes"), ("glicose", "Glicose"),
        ("imagem", "Imagem (Raio-X, Tomografia, etc)"),
        ("colesterol", "Colesterol"), ("hormonal", "Hormonal"),
        ("outro", "Outro")
    ])
    periodo = models.CharField(max_length=20, choices=[
        ("ate_6_meses", "Entre 1 e 6 meses"), ("mais_6_meses", "Mais de 6 meses")
    ])
    arquivo = models.FileField(upload_to=exame_upload_path)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.nome} - {self.get_tipo_display()} ({self.periodo})"
