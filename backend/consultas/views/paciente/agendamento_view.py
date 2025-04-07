from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import get_object_or_404
from consultas.models import (
    Consulta,
    TicketReembolso,
    EventoConsulta,
    Notificacao
)
from consultas.serializers import ConsultaSerializer


class MinhasConsultasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paciente = request.user
        consultas = Consulta.objects.filter(paciente=paciente).order_by('-data_hora')
        serializer = ConsultaSerializer(consultas, many=True)
        return Response(serializer.data)


class AgendarConsultaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['paciente'] = request.user.id  # força o paciente a ser ele mesmo
        serializer = ConsultaSerializer(data=data)
        if serializer.is_valid():
            consulta = serializer.save()

            # 📋 Evento de agendamento
            EventoConsulta.objects.create(
                consulta=consulta,
                usuario=request.user,
                tipo_evento='agendamento',
                observacao='Consulta agendada pelo paciente.'
            )

            # 📬 Notifica colaborador (ex: admin ID 1)
            Notificacao.objects.create(
                usuario_id=1,
                titulo="Nova Consulta Agendada",
                mensagem=f"{request.user.nome} agendou uma nova consulta."
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelarConsultaView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, consulta_id):
        consulta = get_object_or_404(Consulta, id=consulta_id, paciente=request.user)

        if consulta.status in ['cancelada', 'realizada']:
            return Response({"detail": "Consulta não pode ser cancelada."}, status=status.HTTP_400_BAD_REQUEST)

        consulta.status = 'cancelada'
        consulta.cancelado_por = request.user
        consulta.save()

        if consulta.metodo_pagamento in ['pix', 'credito', 'debito'] and consulta.pagamento_confirmado:
            TicketReembolso.objects.create(
                consulta=consulta,
                paciente=request.user,
                valor_total=150.00,
                metodo_pagamento=consulta.metodo_pagamento,
                motivo="Cancelamento pelo paciente"
            )

        EventoConsulta.objects.create(
            consulta=consulta,
            usuario=request.user,
            tipo_evento='cancelamento',
            observacao='Cancelamento solicitado pelo paciente.'
        )

        Notificacao.objects.create(
            usuario_id=1,
            titulo="Consulta Cancelada",
            mensagem=f"A consulta do paciente {request.user.nome} foi cancelada e precisa de avaliação para possível reembolso."
        )

        return Response({"detail": "Consulta cancelada com sucesso."}, status=status.HTTP_200_OK)
