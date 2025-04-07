from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.permissions import IsMedico, IsMedicoOrAdmin
from consultas.models import (
    Consulta, EventoConsulta, TicketConciliacaoFinanceira,
    RepasseMedico, RelatorioConsulta
)
from rest_framework.generics import get_object_or_404
from django.utils import timezone
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.base import ContentFile
import tempfile
import os
from consultas.utils.gerador_resumo import gerar_resumo_paciente


class FinalizarConsultaView(APIView):
    permission_classes = [IsAuthenticated, IsMedico]

    def post(self, request, consulta_id):
        consulta = Consulta.objects.filter(id=consulta_id, medico=request.user).first()
        if not consulta:
            return Response({"detail": "Consulta não encontrada."}, status=404)

        if consulta.status == "realizada":
            return Response({"detail": "Consulta já finalizada."}, status=400)

        # 🧠 Gera introdução automática
        resumo = gerar_resumo_paciente(consulta)

        # ✍️ Cria o relatório
        relatorio = RelatorioConsulta.objects.create(
            consulta=consulta,
            cid10=request.data.get("cid10", ""),
            descricao_complementar=request.data.get("descricao_complementar", ""),
            exames_solicitados=request.data.get("exames_solicitados", ""),
            tratamento_orientado=request.data.get("tratamento_orientado", ""),
            introducao_gerada=resumo,
            visivel_para_paciente=request.data.get("visivel_para_paciente", False)
        )

        # ✅ Marca como finalizada
        consulta.status = "realizada"
        consulta.comparecimento = True
        consulta.save()

        # 🧾 Gera PDF automaticamente
        context = {
            "consulta": consulta,
            "relatorio": relatorio,
        }
        html_string = render_to_string("relatorio/relatorio_pdf.html", context)
        html = HTML(string=html_string)
        pdf_file = html.write_pdf()

        # 💾 Salva o PDF na model se quiser (ex: campo FileField futuramente)

        # 🔗 Retorna URL para visualização do PDF (ajustável para frontend)
        pdf_url = f"/api/consultas/medico/consulta/{consulta.id}/relatorio/pdf/"

        return Response({
            "detail": "Consulta finalizada com sucesso e relatório gerado.",
            "resumo_gerado": resumo,
            "pdf_url": pdf_url
        }, status=status.HTTP_201_CREATED)


class FinalizarAtendimentoView(APIView):
    permission_classes = [IsAuthenticated, IsMedico]

    def post(self, request, consulta_id):
        consulta = Consulta.objects.filter(id=consulta_id, medico=request.user).first()
        if not consulta:
            return Response({"detail": "Consulta não encontrada."}, status=404)

        if consulta.status == "realizada":
            return Response({"detail": "Consulta já finalizada."}, status=400)

        introducao = gerar_resumo_paciente(consulta)

        relatorio, created = RelatorioConsulta.objects.get_or_create(
            consulta=consulta,
            defaults={
                "introducao_gerada": introducao,
                "descricao_complementar": request.data.get("descricao_complementar", ""),
                "cid10": request.data.get("cid10", ""),
                "exames_solicitados": request.data.get("exames_solicitados", ""),
                "tratamento_orientado": request.data.get("tratamento_orientado", ""),
                "visivel_para_paciente": request.data.get("visivel_para_paciente", False),
            }
        )

        consulta.status = "realizada"
        consulta.comparecimento = True
        consulta.save()

        return Response({
            "detail": "Consulta finalizada e relatório criado.",
            "resumo_gerado": introducao
        }, status=status.HTTP_201_CREATED)
