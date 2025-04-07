from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail  # ou notificação no sistema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from users.models import CustomUser
from consultas.models import Consulta
from django.utils.crypto import get_random_string

class GerarLinksTelemedicinaView(APIView):
    permission_classes = [IsAdminUser]  # Ou crie permissão custom se quiser refinar

    def post(self, request):
        agora = timezone.now()
        limite = agora + timedelta(minutes=30)

        consultas = Consulta.objects.filter(
            is_telemedicina=True,
            link_telemedicina__isnull=True,
            data_hora__range=(agora, limite),
            status='marcada'
        )

        total = 0
        for consulta in consultas:
            codigo = get_random_string(12)
            consulta.link_telemedicina = f"https://meet.jit.si/consulta_{codigo}"
            consulta.save()
            total += 1

            # 💌 Notificar médico e paciente (ou logar evento)
            print(f"[+] Link gerado para consulta {consulta.id} | {consulta.link_telemedicina}")

        return Response({
            "detail": f"{total} link(s) gerado(s) com sucesso."
        })
