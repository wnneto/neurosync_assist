from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from consultas.models import EventoConsulta
from users.permissions import IsColaborador
from rest_framework.generics import get_object_or_404
from consultas.models import Consulta

class EventosPorConsultaView(APIView):
    permission_classes = [IsAuthenticated, IsColaborador]

    def get(self, request, consulta_id):
        consulta = get_object_or_404(Consulta, id=consulta_id)
        eventos = EventoConsulta.objects.filter(consulta=consulta).order_by('data_hora')
        data = [
            {
                "tipo": e.tipo_evento,
                "usuario": e.usuario.nome if e.usuario else "Sistema",
                "observacao": e.observacao,
                "data_hora": e.data_hora
            }
            for e in eventos
        ]
        return Response(data)
