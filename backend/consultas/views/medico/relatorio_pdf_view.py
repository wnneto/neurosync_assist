from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from consultas.models import Consulta, RelatorioConsulta
from users.permissions import IsMedicoOrAdmin

class GerarPDFRelatorioConsultaView(APIView):
    permission_classes = [IsAuthenticated, IsMedicoOrAdmin]

    def get(self, request, consulta_id):
        consulta = get_object_or_404(Consulta, id=consulta_id, medico=request.user)

        try:
            relatorio = RelatorioConsulta.objects.get(consulta=consulta)
        except RelatorioConsulta.DoesNotExist:
            return HttpResponse("Relatório não encontrado.", status=404)

        html_string = render_to_string("relatorio/relatorio_pdf.html", {
            "consulta": consulta,
            "relatorio": relatorio,
        })

        html = HTML(string=html_string)
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename=relatorio_consulta_{consulta.id}.pdf'
        return response
