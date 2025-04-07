# consultas/models/notificacao.py

from django.db import models
from users.models import CustomUser

class Notificacao(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notificacoes')
    titulo = models.CharField(max_length=100)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    enviada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.usuario.nome}: {self.titulo}"
