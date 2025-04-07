# users/views/profile_views.py

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from users.serializers import UserProfileSerializer
from consultas.models import Consulta
from fichamedica.models import DadosMedicos
from fichamedica.serializers.medico_serializers import DadosMedicosSerializer
from consultas.serializers import ConsultaResumoSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PacienteCompletoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, paciente_id):
        paciente = get_object_or_404(CustomUser, id=paciente_id)
        dados_medicos = DadosMedicos.objects.filter(usuario=paciente).first()
        historico = Consulta.objects.filter(paciente=paciente).order_by("-data")

        return Response({
            "id": paciente.id,
            "nome": paciente.nome,
            "email": paciente.email,
            "cpf": paciente.cpf,
            "sexo": paciente.sexo,
            "data_nascimento": paciente.data_nascimento,
            "dados_medicos": DadosMedicosSerializer(dados_medicos).data if dados_medicos else {},
            "historico": ConsultaResumoSerializer(historico, many=True).data
        })
