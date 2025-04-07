# users/serializers/colaborador_serializers.py

from rest_framework import serializers
from users.models import CustomUser

class UsuarioAdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'nome', 'email', 'perfil', 'is_active', 'date_joined']
