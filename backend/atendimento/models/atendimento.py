from django.db import models
from consultas.models import Consulta  # Agora puxando da app correta

class Atendimento(models.Model):
    consulta = models.OneToOneField(
        Consulta,
        on_delete=models.CASCADE,
        related_name="atendimento"
    )
    relatorio = models.TextField()
    cid = models.CharField(max_length=20, blank=True, null=True)
    exames_solicitados = models.TextField(blank=True)
    tratamento_recomendado = models.TextField(blank=True)
    link_telemedicina = models.URLField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    inicio_telemedicina = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"Atendimento da Consulta #{self.consulta_id}"
