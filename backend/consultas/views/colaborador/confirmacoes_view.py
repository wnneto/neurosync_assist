from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsColaborador
from consultas.models import Consulta, EventoConsulta
from consultas.serializers import ConsultaSerializer
from rest_framework import status

class ConfirmacoesPendentesView(APIView):
    permission_classes = [IsAuthenticated, IsColaborador]

    def get(self, request):
        consultas = Consulta.objects.filter(
            status__in=["remarcacao_pendente", "realizada", "marcada"]
        ).filter(
            pagamento_confirmado=False
        ).order_by("data_hora")

        serializer = ConsultaSerializer(consultas, many=True)
        return Response(serializer.data)


class AtualizarConfirmacaoConsultaView(APIView):
    permission_classes = [IsAuthenticated, IsColaborador]

    def patch(self, request, consulta_id):
        consulta = Consulta.objects.filter(id=consulta_id).first()
        if not consulta:
            return Response({"detail": "Consulta não encontrada."}, status=404)

        aprovacao = request.data.get("aprovacao")
        confirmar_pagamento = request.data.get("pagamento_confirmado")

        if aprovacao == "aceita":
            consulta.status = "marcada"
            observacao = "Remarcação aprovada pelo colaborador."
        elif aprovacao == "recusada":
            consulta.status = "cancelada"
            observacao = "Remarcação recusada pelo colaborador."
        elif confirmar_pagamento:
            consulta.pagamento_confirmado = True
            observacao = "Pagamento confirmado pelo colaborador."
        else:
            return Response({"detail": "Nada para atualizar."}, status=400)

        consulta.save()

        EventoConsulta.objects.create(
            consulta=consulta,
            usuario=request.user,
            tipo_evento="remarcacao_aprovada" if aprovacao == "aceita" else "cancelamento" if aprovacao == "recusada" else "pagamento",
            observacao=observacao
        )

        return Response({"detail": "Consulta atualizada com sucesso."}, status=200)
