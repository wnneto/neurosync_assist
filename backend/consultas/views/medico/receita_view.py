from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from users.permissions import IsMedicoOrAdmin
from consultas.models import Consulta, ReceitaMedica
from django.core.files.base import ContentFile

class CriarReceitaMedicaView(APIView):
    permission_classes = [IsAuthenticated, IsMedicoOrAdmin]

    def post(self, request, consulta_id):
        consulta = get_object_or_404(Consulta, id=consulta_id, medico=request.user)

        conteudo = request.data.get("conteudo", "")
        visivel = request.data.get("visivel_para_paciente", False)

        receita, created = ReceitaMedica.objects.get_or_create(
            consulta=consulta,
            defaults={
                "conteudo": conteudo,
                "visivel_para_paciente": visivel
            }
        )

        if not created:
            receita.conteudo = conteudo
            receita.visivel_para_paciente = visivel
            receita.save()

        html_string = render_to_string("receitas/receita_pdf.html", {
            "consulta": consulta,
            "receita": receita,
        })

        pdf_file = HTML(string=html_string).write_pdf()

        receita.arquivo_pdf.save(
            f"receita_consulta_{consulta.id}.pdf",
            ContentFile(pdf_file)
        )

        return HttpResponse(pdf_file, content_type="application/pdf")
