from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from atendimento.models.atendimento import Consulta
class IniciarTelemedicinaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, consulta_id):
        consulta = get_object_or_404(Consulta, id=consulta_id)
        atendimento = consulta.atendimento

        if not atendimento.link_telemedicina:
            atendimento.link_telemedicina = f"https://meet.jit.si/consulta_{consulta_id}"

        if not atendimento.inicio_telemedicina:
            atendimento.inicio_telemedicina = now()

        atendimento.save()

        return Response({
            "link_telemedicina": atendimento.link_telemedicina,
            "inicio_telemedicina": atendimento.inicio_telemedicina
        })
