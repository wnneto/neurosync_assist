from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from consultas.models import Consulta
from consultas.serializers import ConsultaSerializer

class HistoricoConsultasPacienteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        consultas = Consulta.objects.filter(paciente=request.user).order_by("-data_hora")
        serializer = ConsultaSerializer(consultas, many=True)
        return Response(serializer.data)
