from django.db import models
from consultas.models import Consulta
from users.models import CustomUser

class TicketConciliacaoFinanceira(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, related_name="conciliacao")
    valor_consulta = models.DecimalField(max_digits=8, decimal_places=2)
    metodo_pagamento = models.CharField(max_length=20, choices=[
        ('pix', 'Pix'),
        ('credito', 'Crédito'),
        ('debito', 'Débito'),
        ('dinheiro', 'Dinheiro'),
        ('convenio', 'Convênio'),
    ])
    conciliado = models.BooleanField(default=False)
    confirmado_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    data_conciliacao = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket - Consulta {self.consulta.id} - {self.metodo_pagamento}"
