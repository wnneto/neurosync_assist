from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from consultas.models import TicketReembolso, EventoConsulta, Notificacao
from users.permissions import IsColaborador

class ListaTicketsReembolsoView(APIView):
    permission_classes = [IsAuthenticated, IsColaborador]

    def get(self, request):
        tickets = TicketReembolso.objects.filter(aprovado__isnull=True)
        data = [
            {
                "id": t.id,
                "paciente": t.paciente.nome,
                "consulta_id": t.consulta.id,
                "valor_total": float(t.valor_total),
                "percentual_reembolso": t.percentual_reembolso,
                "metodo": t.metodo_pagamento,
                "motivo": t.motivo,
                "criado_em": t.criado_em,
            }
            for t in tickets
        ]
        return Response(data)


class AprovarReembolsoView(APIView):
    permission_classes = [IsAuthenticated, IsColaborador]

    def post(self, request, ticket_id):
        ticket = TicketReembolso.objects.filter(id=ticket_id).first()
        if not ticket:
            return Response({"detail": "Ticket não encontrado."}, status=404)

        aprovado = request.data.get("aprovado")
        percentual = request.data.get("percentual_reembolso", ticket.percentual_reembolso)

        ticket.aprovado = bool(aprovado)
        ticket.percentual_reembolso = percentual
        ticket.save()

        # Registra evento
        EventoConsulta.objects.create(
            consulta=ticket.consulta,
            usuario=request.user,
            tipo_evento='remarcacao_aprovada' if aprovado else 'cancelamento',
            observacao='Reembolso analisado pelo colaborador.'
        )

        # Notifica paciente
        Notificacao.objects.create(
            usuario=ticket.paciente,
            titulo="Reembolso analisado",
            mensagem=f"Seu reembolso foi {'aprovado' if aprovado else 'recusado'} com {percentual}% do valor."
        )

        return Response({"detail": "Decisão registrada com sucesso."})



