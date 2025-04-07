# fichamedica/models/documentos.py

from django.db import models
from django.conf import settings


def exame_upload_path(instance, filename):
    return f"exames/{instance.usuario.id}/{filename}"


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
