from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsColaborador
from consultas.models import TicketConciliacaoFinanceira
from consultas.models import EventoConsulta


class ListaTicketsConsolidacaoView(APIView):
    permission_classes = [IsAuthenticated, IsColaborador]

    def get(self, request):
        tickets = TicketConciliacaoFinanceira.objects.filter(conciliado=False).order_by("criado_em")
        data = [
            {
                "id": t.id,
                "consulta_id": t.consulta.id,
                "paciente": t.consulta.paciente.nome,
                "medico": t.consulta.medico.nome if t.consulta.medico else "Não definido",
                "data_consulta": t.consulta.data_hora,
                "valor": float(t.valor_consulta),
                "metodo_pagamento": t.metodo_pagamento,
                "vencimento": t.data_conciliacao,
                "conciliado": t.conciliado
            }
            for t in tickets
        ]
        return Response(data)



class EditarConciliacaoView(APIView):
    permission_classes = [IsAuthenticated, IsColaborador]

    def patch(self, request, ticket_id):
        ticket = get_object_or_404(TicketConciliacaoFinanceira, id=ticket_id)
        consulta = ticket.consulta
        user = request.user

        # Campos que podem ser atualizados
        valor = request.data.get("valor_consulta")
        metodo = request.data.get("metodo_pagamento")
        vencimento = request.data.get("data_conciliacao")
        marcar_conciliado = request.data.get("conciliado")
        reabrir = request.data.get("reabrir")

        log_msg = []

        if reabrir:
            ticket.conciliado = False
            ticket.confirmado_por = None
            ticket.data_conciliacao = None
            log_msg.append("Conciliacao reaberta pelo colaborador.")

        if valor:
            ticket.valor_consulta = valor
            log_msg.append(f"Valor ajustado para R$ {valor}.")

        if metodo:
            ticket.metodo_pagamento = metodo
            log_msg.append(f"Método de pagamento alterado para {metodo}.")

        if vencimento:
            ticket.data_conciliacao = vencimento
            log_msg.append(f"Vencimento atualizado para {vencimento}.")

        if marcar_conciliado:
            ticket.conciliado = True
            ticket.confirmado_por = user
            ticket.data_conciliacao = ticket.data_conciliacao or timezone.now()
            log_msg.append("Conciliacao confirmada.")

        ticket.save()

        if log_msg:
            EventoConsulta.objects.create(
                consulta=consulta,
                usuario=user,
                tipo_evento="conciliacao",
                observacao=" | ".join(log_msg)
            )

        return Response({"detail": "Ticket atualizado com sucesso."}, status=200)