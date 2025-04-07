from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsMedico
from datetime import datetime
from consultas.models import RepasseMedico
import pandas as pd
from fpdf import FPDF
from django.http import FileResponse
import os



# EXCEL FILES

class ExportarRepassesMedicoExcelView(APIView):
    permission_classes = [IsAuthenticated, IsMedico]

    def get(self, request):
        medico = request.user
        inicio = request.GET.get("inicio")  # DD-MM-YYYY
        fim = request.GET.get("fim")        # DD-MM-YYYY

        repasses = RepasseMedico.objects.filter(medico=medico, confirmado=True)

        if inicio and fim:
            try:
                inicio_date = datetime.strptime(inicio, "%d-%m-%Y")
                fim_date = datetime.strptime(fim, "%d-%m-%Y")
                repasses = repasses.filter(consulta__data_hora__date__range=(inicio_date, fim_date))
            except:
                return Response({"detail": "Formato de data inválido. Use DD-MM-YYYY."}, status=400)

        data = [
            {
                "Consulta ID": r.consulta.id,
                "Data": r.consulta.data_hora.strftime("%d-%m-%Y"),
                "Valor Total (R$)": float(r.valor_total_consulta),
                "Percentual": float(r.percentual_repasse),
                "Valor Repassado (R$)": float(r.valor_repassado),
                "Desconto (R$)": float(r.desconto),
                "Descrição": r.descricao_desconto or "",
            }
            for r in repasses
        ]

        total_repassado = sum([float(r.valor_repassado) for r in repasses])
        df = pd.DataFrame(data)
        df.loc["Total"] = ["", "", "", "", total_repassado, "", ""]

        file_path = "/tmp/repasses_medico.xlsx"
        df.to_excel(file_path, index=False)
        return FileResponse(open(file_path, "rb"), as_attachment=True, filename="repasses_medico.xlsx")


# PDF FILES


class ExportarRepassesMedicoPDFView(APIView):
    permission_classes = [IsAuthenticated, IsMedico]

    def get(self, request):
        medico = request.user
        inicio = request.GET.get("inicio")
        fim = request.GET.get("fim")

        repasses = RepasseMedico.objects.filter(medico=medico, confirmado=True)

        if inicio and fim:
            try:
                inicio_date = datetime.strptime(inicio, "%d-%m-%Y")
                fim_date = datetime.strptime(fim, "%d-%m-%Y")
                repasses = repasses.filter(consulta__data_hora__date__range=(inicio_date, fim_date))
            except:
                return Response({"detail": "Formato de data inválido. Use DD-MM-YYYY."}, status=400)

        data = [
            {
                "Consulta ID": r.consulta.id,
                "Data": r.consulta.data_hora.strftime("%d-%m-%Y"),
                "Valor": f"R$ {r.valor_repassado:.2f}",
            }
            for r in repasses
        ]
        total = sum([float(r.valor_repassado) for r in repasses])

        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 12)
                self.cell(0, 10, "Repasses Confirmados - NeuralSync", 0, 1, "C")
                self.ln(5)

            def table(self, data, total):
                self.set_font("Arial", "B", 10)
                headers = ["Consulta ID", "Data", "Valor"]
                col_widths = [40, 50, 50]
                for i, header in enumerate(headers):
                    self.cell(col_widths[i], 8, header, 1, 0, "C")
                self.ln()
                self.set_font("Arial", "", 10)
                for row in data:
                    self.cell(col_widths[0], 8, str(row["Consulta ID"]), 1, 0, "C")
                    self.cell(col_widths[1], 8, row["Data"], 1, 0, "C")
                    self.cell(col_widths[2], 8, row["Valor"], 1, 0, "C")
                    self.ln()
                self.set_font("Arial", "B", 10)
                self.cell(col_widths[0] + col_widths[1], 8, "TOTAL", 1, 0, "C")
                self.cell(col_widths[2], 8, f"R$ {total:.2f}", 1, 0, "C")

        pdf = PDF()
        pdf.add_page()
        pdf.table(data, total)
        file_path = "/tmp/repasses_medico.pdf"
        pdf.output(file_path)
        return FileResponse(open(file_path, "rb"), as_attachment=True, filename="repasses_medico.pdf")
