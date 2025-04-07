# fichamedica/views/paciente_views.py

from rest_framework import generics, permissions, parsers
from fichamedica.models import DadosMedicos, Anamnese, Exame
from fichamedica.serializers.medico_serializers import DadosMedicosSerializer, AnamneseSerializer, ExameSerializer


# --- DADOS MÉDICOS ---
class DadosMedicosView(generics.RetrieveUpdateAPIView):
    serializer_class = DadosMedicosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = DadosMedicos.objects.get_or_create(usuario=self.request.user)
        return obj


# --- ANAMNESE ---
class AnamneseView(generics.RetrieveUpdateAPIView):
    serializer_class = AnamneseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = Anamnese.objects.get_or_create(usuario=self.request.user)
        return obj


# --- EXAMES ---
class ExameListCreateView(generics.ListCreateAPIView):
    serializer_class = ExameSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_queryset(self):
        return Exame.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ExameDeleteView(generics.DestroyAPIView):
    serializer_class = ExameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Exame.objects.filter(usuario=self.request.user)
