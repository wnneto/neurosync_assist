# users/views/colaborador_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.permissions import IsColaborador
from users.models import CustomUser
from users.serializers.colaborador_serializers import UsuarioAdminListSerializer
from users.serializers import UsuarioSerializer


class ListaUsuariosView(APIView):
    permission_classes = [IsAuthenticated, IsColaborador]

    def get(self, request):
        usuarios = CustomUser.objects.all()
        serializer = UsuarioAdminListSerializer(usuarios, many=True)
        return Response(serializer.data)

class ListaUsuariosView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        usuarios = CustomUser.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
