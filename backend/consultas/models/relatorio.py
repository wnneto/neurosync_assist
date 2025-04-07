from django.db import models
from consultas.models import Consulta

class RelatorioConsulta(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, related_name='relatorio')
    
    introducao_gerada = models.TextField(blank=True, help_text="Resumo automático que pode ser editado ou descartado.")
    descricao_complementar = models.TextField(blank=True, help_text="Texto livre do médico.")
    cid10 = models.CharField(max_length=20, blank=True, help_text="CID-10 da condição principal.")
    exames_solicitados = models.TextField(blank=True, help_text="Descrição dos exames solicitados.")
    tratamento_orientado = models.TextField(blank=True, help_text="Conduta e orientações passadas ao paciente.")
    
    visivel_para_paciente = models.BooleanField(default=False, help_text="Se marcado, o paciente poderá ver esse relatório.")
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Relatório da Consulta #{self.consulta.id}'
