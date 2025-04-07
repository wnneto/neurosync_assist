from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from consultas.models import Consulta
from django.http import FileResponse
from fpdf import FPDF
from datetime import datetime

class EmitirReciboConsultaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, consulta_id):
        consulta = get_object_or_404(Consulta, id=consulta_id, paciente=request.user)

        if consulta.status != "realizada" or not consulta.pagamento_confirmado:
            return Response({"detail": "Recibo não disponível."}, status=400)

        valor = consulta.conciliacao.valor_consulta if hasattr(consulta, "conciliacao") else 150.00
        metodo = consulta.metodo_pagamento or "Não informado"
        medico = consulta.medico.nome if consulta.medico else "Profissional não definido"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "NEURALSYNC - RECIBO DE CONSULTA", 0, 1, "C")
        pdf.ln(10)

        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, f"""
Paciente: {request.user.nome}
Data da Consulta: {consulta.data_hora.strftime('%d/%m/%Y')}
Profissional: {medico}
Serviço Prestado: Consulta médica
Forma de Pagamento: {metodo}
Valor: R$ {valor:.2f}

Emitido em: {datetime.now().strftime('%d/%m/%Y')}
""")

        file_path = "/tmp/recibo_consulta.pdf"
        pdf.output(file_path)
        return FileResponse(open(file_path, "rb"), as_attachment=True, filename="recibo_consulta.pdf")
