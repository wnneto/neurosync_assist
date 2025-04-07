# consultas/models/ticket.py

from django.db import models
from users.models import CustomUser
from consultas.models import Consulta

class TicketReembolso(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='tickets')
    paciente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2)
    percentual_reembolso = models.IntegerField(default=100)  # até 100%
    metodo_pagamento = models.CharField(max_length=20, choices=[
        ('pix', 'Pix'),
        ('credito', 'Crédito'),
        ('debito', 'Débito'),
    ])
    motivo = models.TextField(blank=True, null=True)
    aprovado = models.BooleanField(null=True)  # None = pendente
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reembolso de R${self.valor_total} para {self.paciente.nome}"
