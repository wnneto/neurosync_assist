from rest_framework import generics, permissions
from fichamedica.models.fatores import FatorClimatico
from fichamedica.serializers.fatores_serializers import FatorClimaticoSerializer


class FatorClimaticoListView(generics.ListAPIView):
    queryset = FatorClimatico.objects.all().order_by('nome')
    serializer_class = FatorClimaticoSerializer
    permission_classes = [permissions.AllowAny]