from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Count, Avg, Q, F, Sum
from datetime import datetime, timedelta
from consultas.models import Consulta, EventoConsulta, TicketReembolso, RepasseMedico
from users.models import CustomUser
from django.http import FileResponse
import pandas as pd
from fpdf import FPDF
import os

class RelatorioGeralAdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            inicio_str = request.GET.get("inicio")
            fim_str = request.GET.get("fim")
            if inicio_str and fim_str:
                inicio = datetime.strptime(inicio_str, "%d-%m-%Y")
                fim = datetime.strptime(fim_str, "%d-%m-%Y")
            else:
                fim = datetime.now()
                inicio = fim - timedelta(days=30)
        except:
            return Response({"detail": "Formato de data inválido. Use DD-MM-YYYY."}, status=400)

        sexo = request.GET.get("sexo")
        categoria = request.GET.get("categoria")
        faixa_etaria = request.GET.get("faixa_etaria")

        consultas = Consulta.objects.filter(data_hora__range=(inicio, fim))

        if sexo:
            consultas = consultas.filter(paciente__sexo=sexo)

        if categoria:
            consultas = consultas.filter(paciente__grupo=categoria)

        if faixa_etaria:
            hoje = datetime.today().date()
            try:
                idade_min, idade_max = map(int, faixa_etaria.split("-"))
                data_nascimento_min = hoje.replace(year=hoje.year - idade_max)
                data_nascimento_max = hoje.replace(year=hoje.year - idade_min)
                consultas = consultas.filter(paciente__data_nascimento__range=(data_nascimento_min, data_nascimento_max))
            except:
                return Response({"detail": "Formato de faixa_etaria inválido. Use EX: 18-30."}, status=400)

        total_consultas = consultas.count()
        realizadas = consultas.filter(status="realizada").count()
        canceladas = consultas.filter(status="cancelada").count()
        marcadas = consultas.filter(status="marcada").count()
        retornos_gerados = consultas.exclude(consulta_original=None).count()

        total_conciliado = RepasseMedico.objects.filter(
            consulta__data_hora__range=(inicio, fim), confirmado=True
        ).aggregate(total=Sum("valor_repassado"))['total'] or 0

        reembolsos_abertos = TicketReembolso.objects.filter(
            consulta__data_hora__range=(inicio, fim), finalizado=False
        ).count()

        medicos = CustomUser.objects.filter(grupo="medico")
        atendimentos_por_medico = {
            medico.nome: consultas.filter(medico=medico, status="realizada").count()
            for medico in medicos
        }

        tickets_ativos = TicketReembolso.objects.filter(
            consulta__data_hora__range=(inicio, fim), finalizado=False
        ).count()
        remarcacoes_pendentes = EventoConsulta.objects.filter(
            consulta__data_hora__range=(inicio, fim), tipo_evento="remarcacao_pendente"
        ).count()

        if request.GET.get("export") == "excel":
            df = pd.DataFrame([{
                "Total de Consultas": total_consultas,
                "Realizadas": realizadas,
                "Canceladas": canceladas,
                "Marcadas": marcadas,
                "Retornos Gerados": retornos_gerados,
                "Total Conciliado (R$)": total_conciliado,
                "Reembolsos Abertos": reembolsos_abertos,
                "Tickets Ativos": tickets_ativos,
                "Remarcações Pendentes": remarcacoes_pendentes
            }])
            file_path = "/tmp/relatorio_admin.xlsx"
            df.to_excel(file_path, index=False)
            return FileResponse(open(file_path, "rb"), as_attachment=True, filename="relatorio_admin.xlsx")

        if request.GET.get("export") == "pdf":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Relatório Geral Administrativo - NeuralSync", 0, 1, "C")
            pdf.set_font("Arial", "", 12)
            pdf.ln(10)
            linhas = [
                f"Período: {inicio.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}",
                f"Total de Consultas: {total_consultas}",
                f" - Realizadas: {realizadas}",
                f" - Canceladas: {canceladas}",
                f" - Marcadas: {marcadas}",
                f" - Retornos: {retornos_gerados}",
                f"Total Conciliado: R$ {total_conciliado:.2f}",
                f"Reembolsos Abertos: {reembolsos_abertos}",
                f"Tickets Ativos: {tickets_ativos}",
                f"Remarcações Pendentes: {remarcacoes_pendentes}"
            ]
            for linha in linhas:
                pdf.cell(0, 10, linha, 0, 1)
            file_path = "/tmp/relatorio_admin.pdf"
            pdf.output(file_path)
            return FileResponse(open(file_path, "rb"), as_attachment=True, filename="relatorio_admin.pdf")

        return Response({
            "periodo": f"{inicio.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}",
            "filtros": {
                "sexo": sexo,
                "categoria": categoria,
                "faixa_etaria": faixa_etaria
            },
            "volume": {
                "total": total_consultas,
                "realizadas": realizadas,
                "canceladas": canceladas,
                "marcadas": marcadas,
                "retornos_gerados": retornos_gerados
            },
            "financeiro": {
                "total_conciliado": float(total_conciliado),
                "reembolsos_abertos": reembolsos_abertos
            },
            "atividades_admin": {
                "tickets_abertos": tickets_ativos,
                "remarcacoes_pendentes": remarcacoes_pendentes
            },
            "desempenho_medico": atendimentos_por_medico
        })