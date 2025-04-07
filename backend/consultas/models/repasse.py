from django.db import models
from users.models import CustomUser
from consultas.models import Consulta
import uuid

class RepasseMedico(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, related_name='repasse')
    medico = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='repasse_medico')
    pagamento_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    percentual_repasse = models.DecimalField(max_digits=5, decimal_places=2, default=50.00)  # Ex: 50%
    valor_total_consulta = models.DecimalField(max_digits=8, decimal_places=2)
    valor_repassado = models.DecimalField(max_digits=8, decimal_places=2)
    desconto = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    descricao_desconto = models.TextField(blank=True, null=True)
    confirmado = models.BooleanField(default=False)
    data_confirmacao = models.DateTimeField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Repasse #{self.pagamento_id} - Médico: {self.medico.nome}"
