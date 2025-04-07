from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsColaborador
from consultas.models import Consulta
from consultas.serializers import ConsultaSerializer
from django.utils import timezone

class AgendaGeralView(APIView):
    permission_classes = [IsAuthenticated, IsColaborador]

    def get(self, request):
        # Filtros opcionais
        data = request.query_params.get("data")  # formato YYYY-MM-DD
        status = request.query_params.get("status")
        medico_id = request.query_params.get("medico_id")

        consultas = Consulta.objects.all()

        if data:
            consultas = consultas.filter(data_hora__date=data)
        if status:
            consultas = consultas.filter(status=status)
        if medico_id:
            consultas = consultas.filter(medico_id=medico_id)

        consultas = consultas.order_by("data_hora")
        serializer = ConsultaSerializer(consultas, many=True)
        return Response(serializer.data)
