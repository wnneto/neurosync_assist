from django.db import models
from users.models import CustomUser


class Consulta(models.Model):
    paciente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="consultas_paciente")
    medico = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="consultas_medico")
    data = models.DateTimeField(auto_now_add=True)
    modalidade = models.CharField(
        max_length=20,
        choices=[("presencial", "Presencial"), ("telemedicina", "Telemedicina")],
        default="presencial"
    )
    status = models.CharField(
        max_length=20,
        choices=[("agendada", "Agendada"), ("realizada", "Realizada"), ("cancelada", "Cancelada")],
        default="agendada"
    )
    comparecimento = models.BooleanField(default=False)

    def __str__(self):
        return f"Consulta #{self.id} - {self.paciente.get_full_name()}"
