from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from atendimento.models import DocumentoConsulta
from atendimento.serializers.documento_serializer import DocumentoConsultaSerializer

class DocumentoConsultaCreateView(generics.CreateAPIView):
    queryset = DocumentoConsulta.objects.all()
    serializer_class = DocumentoConsultaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.grupo != "medico":
            raise PermissionDenied("Apenas médicos podem emitir documentos.")
        serializer.save()
