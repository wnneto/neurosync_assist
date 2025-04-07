from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import get_object_or_404
from users.permissions import IsMedicoOrColaborador
from consultas.models import Consulta, CustomUser


class AtribuirMedicoView(APIView):
    permission_classes = [IsAuthenticated, IsMedicoOrColaborador]

    def post(self, request, consulta_id):
        consulta = get_object_or_404(Consulta, id=consulta_id)

        if getattr(request.user, 'grupo', None) == 'medico':
            consulta.medico = request.user
        else:
            medico_id = request.data.get("medico_id")
            if not medico_id:
                return Response({"detail": "ID do médico não informado."}, status=400)

            try:
                medico = CustomUser.objects.get(id=medico_id, grupo="medico")
            except CustomUser.DoesNotExist:
                return Response({"detail": "Médico não encontrado."}, status=404)

            consulta.medico = medico

        consulta.save()
        return Response({"detail": f"Médico atribuído com sucesso à consulta {consulta.id}."}, status=200)
