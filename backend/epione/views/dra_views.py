# epione/views/ia_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from epione.models import Doenca, Sintoma
from epione.serializers.sintoma_serializer import SintomaSerializer
from epione.services.ia_service import gerar_raciocinio_clinico
import asyncio

class DiagnosticoIAView(APIView):

    permission_classes = [AllowAny]
    def post(self, request):
        sintomas_ids = request.data.get("sintomas_ids", [])
        historico = request.data.get("historico", "")
        idade = request.data.get("idade", "")
        sexo = request.data.get("sexo", "")

        sintomas = Sintoma.objects.filter(id__in=sintomas_ids)
        sintomas_nomes = ", ".join([s.descricao for s in sintomas])

        # Diagnóstico preliminar baseado no banco de dados
        doencas = Doenca.objects.filter(sintomas__in=sintomas).distinct()
        doencas_nomes = ", ".join([d.descricao for d in doencas])

        prompt = f"""
Paciente do sexo {sexo}, {idade} anos. Histórico relevante: {historico}.
Sintomas atuais: {sintomas_nomes}.
Doenças compatíveis encontradas: {doencas_nomes}.

Com base nesses dados, elabore um raciocínio clínico detalhado, indique suspeitas principais e recomende exames complementares.
"""

        resposta = asyncio.run(gerar_raciocinio_clinico(prompt))

        return Response({
            "diagnostico_ia": resposta,
            "doencas_possiveis": [d.descricao for d in doencas],
        }, status=status.HTTP_200_OK)
