from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsMedico
from consultas.models import Consulta
from consultas.serializers import ConsultaSerializer

class AgendaMedicoView(APIView):
    permission_classes = [IsAuthenticated, IsMedico]

    def get(self, request):
        medico = request.user
        consultas = Consulta.objects.filter(medico=medico).order_by("data_hora")
        serializer = ConsultaSerializer(consultas, many=True)
        return Response(serializer.data)
