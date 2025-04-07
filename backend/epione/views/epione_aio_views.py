# epione/views/epione_all_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from epione.models import Doenca, Sintoma, FatorClimatico, Medicamento
from epione.serializers import (
    DoencaSerializer,
    SintomaSerializer,
    FatorClimaticoSerializer,
    MedicamentoSerializer,
)


class EpioneAllView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "doencas": DoencaSerializer(Doenca.objects.all(), many=True).data,
            "sintomas": SintomaSerializer(Sintoma.objects.all(), many=True).data,
            "fatores_climaticos": FatorClimaticoSerializer(FatorClimatico.objects.all(), many=True).data,
            "medicamentos": MedicamentoSerializer(Medicamento.objects.all(), many=True).data,
        })
