from django.db import models
from django.core.files.base import ContentFile

class ReceitaMedica(models.Model):
    consulta = models.OneToOneField(
        'Consulta', on_delete=models.CASCADE, related_name='receita'
    )
    conteudo = models.TextField(help_text="Conteúdo da receita em texto livre.")
    visivel_para_paciente = models.BooleanField(default=False)
    arquivo_pdf = models.FileField(
        upload_to='receitas/', null=True, blank=True
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Receita da consulta #{self.consulta.id}"
