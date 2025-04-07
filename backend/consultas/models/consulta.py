from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import timedelta
from users.models import CustomUser


class Consulta(models.Model):
    TIPO_CHOICES = [
        ('particular', 'Particular'),
        ('convenio', 'Convênio'),
        ('retorno', 'Retorno'),
    ]

    STATUS_CHOICES = [
        ('marcada', 'Marcada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
        ('remarcacao_pendente', 'Remarcação Pendente'),
        ('confirmada', 'Confirmada'),
    ]

    METODO_PAGAMENTO_CHOICES = [
        ('credito', 'Crédito'),
        ('debito', 'Débito'),
        ('pix', 'Pix'),
        ('dinheiro', 'Dinheiro'),
    ]

    paciente = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='consultas_paciente'
    )

    medico = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultas_medico'
    )

    data_hora = models.DateTimeField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='marcada')

    is_telemedicina = models.BooleanField(default=False)
    link_telemedicina = models.URLField(blank=True, null=True)

    metodo_pagamento = models.CharField(
        max_length=20,
        choices=METODO_PAGAMENTO_CHOICES,
        blank=True,
        null=True
    )
    pagamento_confirmado = models.BooleanField(default=False)
    confirmado_pelo_paciente = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True, null=True)

    consulta_original = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='retornos'
    )

    cancelado_por = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='consultas_canceladas'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def gerar_link_telemedicina(self):
        """Gera um link único via Jitsi se for consulta online"""
        if self.is_telemedicina and not self.link_telemedicina:
            unique_code = get_random_string(12)
            self.link_telemedicina = f"https://meet.jit.si/consulta_{unique_code}"
            self.save(update_fields=['link_telemedicina'])

    def is_retorno_elegivel(self):
        if self.tipo != 'retorno':
            return False
        dias_passados = (timezone.now() - self.consulta_original.data_hora).days if self.consulta_original else 0
        return 7 <= dias_passados <= 30

    def dias_restantes_retorno(self):
        if self.tipo != 'retorno' or not self.consulta_original:
            return None
        data_limite = self.consulta_original.data_hora + timedelta(days=30)
        return (data_limite - timezone.now()).days

    def __str__(self):
        nome_medico = self.medico.nome if self.medico else "Médico indefinido"
        return f"{self.paciente.nome} com {nome_medico} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"




class ReceitaMedica(models.Model):
    consulta = models.OneToOneField('Consulta', on_delete=models.CASCADE)
    conteudo = models.TextField()
    visivel_para_paciente = models.BooleanField(default=False)
    arquivo_pdf = models.FileField(upload_to='receitas/', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receita da Consulta {self.consulta.id}"