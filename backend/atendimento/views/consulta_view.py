from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from atendimento.models import Atendimento
from atendimento.serializers.consulta_serializer import AtendimentoSerializer

class AtendimentoCreateView(generics.CreateAPIView):
    queryset = Atendimento.objects.all()
    serializer_class = AtendimentoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.grupo != "medico":
            raise PermissionDenied("Apenas médicos podem registrar atendimento.")
        serializer.save()
