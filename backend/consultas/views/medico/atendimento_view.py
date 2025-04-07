from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsMedico
from consultas.models import Consulta
from consultas.serializers import ConsultaSerializer
from rest_framework.generics import get_object_or_404

class DetalhesConsultaView(APIView):
    permission_classes = [IsAuthenticated, IsMedico]

    def get(self, request, consulta_id):
        consulta = get_object_or_404(Consulta, id=consulta_id, medico=request.user)
        serializer = ConsultaSerializer(consulta)
        return Response(serializer.data)


class HistoricoAtendimentosView(APIView):
    permission_classes = [IsAuthenticated, IsMedico]

    def get(self, request):
        medico = request.user
        consultas = Consulta.objects.filter(
            medico=medico,
            status="realizada"
        ).order_by("-data_hora")
        serializer = ConsultaSerializer(consultas, many=True)
        return Response(serializer.data)