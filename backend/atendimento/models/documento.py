from django.db import models
from consultas.models import Consulta

class DocumentoConsulta(models.Model):
    TIPOS = [
        ('receita', 'Receita Médica'),
        ('atestado', 'Atestado Médico'),
        ('declaracao', 'Declaração de Comparecimento'),
        ('relatorio', 'Relatório Clínico'),
    ]
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    tipo = models.CharField(choices=TIPOS, max_length=20)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - Consulta #{self.consulta.id}"
