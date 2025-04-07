from rest_framework import generics, permissions
from epione.models.fator_climatico import FatorClimatico
from epione.serializers.fator_climatico_serializer import FatorClimaticoSerializer


class FatorClimaticoListView(generics.ListAPIView):
    queryset = FatorClimatico.objects.all().order_by('nome')
    serializer_class = FatorClimaticoSerializer
    permission_classes = [permissions.AllowAny]
