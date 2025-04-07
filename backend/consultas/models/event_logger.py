# consultas/models/evento.py

from django.db import models
from users.models import CustomUser
from consultas.models import Consulta

class EventoConsulta(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='eventos')
    usuario = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_evento = models.CharField(max_length=30, choices=[
        ('agendamento', 'Agendamento'),
        ('cancelamento', 'Cancelamento'),
        ('presenca', 'Presença Confirmada'),
        ('remarcacao_solicitada', 'Remarcação Solicitada'),
        ('remarcacao_aprovada', 'Remarcação Aprovada'),
        ('no_show', 'Faltou'),
    ])
    observacao = models.TextField(blank=True, null=True)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_evento} - {self.consulta} ({self.data_hora})"
