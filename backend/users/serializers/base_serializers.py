# users/serializers/base_serializers.py

from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer as BaseLoginSerializer
from users.models.base import CustomUser
from users.utils import (
    buscar_endereco_por_cep,
    formatar_cpf,
    validar_cpf,
    formatar_telefone,
    formatar_cep
)
from consultas.models import Consulta
from datetime import datetime


class CustomRegisterSerializer(RegisterSerializer):
    nome = serializers.CharField(required=True)
    sexo = serializers.ChoiceField(choices=CustomUser.SEXO_CHOICES, required=True)
    data_nascimento = serializers.CharField(required=True)
    
    def validate_data_nascimento(self, value):
        try:
            # Aceita tanto DD/MM/YYYY quanto YYYY-MM-DD
            if '/' in value:
                return datetime.strptime(value, '%d/%m/%Y').date()
            else:
                return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise serializers.ValidationError(
                "Formato de data inválido. Use DD/MM/YYYY ou YYYY-MM-DD."
            )
    
    def to_representation(self, instance):
        # Converte para formato BR na saída
        representation = super().to_representation(instance)
        if instance.data_nascimento:
            representation['data_nascimento'] = instance.data_nascimento.strftime('%d/%m/%Y')
        return representation

    telefone = serializers.CharField(required=True)
    cpf = serializers.CharField(required=True)
    cep = serializers.CharField(required=True)
    logradouro = serializers.CharField(required=True)
    numero = serializers.CharField(required=True)
    complemento = serializers.CharField(required=False, allow_blank=True)
    bairro = serializers.CharField(required=True)
    cidade = serializers.CharField(required=True)
    estado = serializers.CharField(required=True)
    pais = serializers.CharField(required=False, default='Brasil')

    username = None  # remove campo username

    def validate_cpf(self, value):
        cpf_formatado = formatar_cpf(value)
        if not validar_cpf(cpf_formatado):
            raise serializers.ValidationError("CPF inválido.")
        if CustomUser.objects.filter(cpf=cpf_formatado).exists():
            raise serializers.ValidationError("Já existe um usuário com este CPF.")
        return cpf_formatado

    def validate_telefone(self, value):
        telefone_formatado = formatar_telefone(value)
        if CustomUser.objects.filter(telefone=telefone_formatado).exists():
            raise serializers.ValidationError("Já existe um usuário com este telefone.")
        return telefone_formatado

    def validate_cep(self, value):
        return formatar_cep(value)

    def validate(self, data):
        endereco = buscar_endereco_por_cep(data.get('cep'))
        if not endereco:
            raise serializers.ValidationError("CEP inválido ou não encontrado.")

        for campo in ['logradouro', 'bairro', 'cidade', 'estado']:
            if not data.get(campo):
                data[campo] = endereco.get(campo, '')

        data['pais'] = data.get('pais', 'Brasil')
        return super().validate(data)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        fields = [
            'nome', 'sexo', 'data_nascimento', 'telefone', 'cpf',
            'cep', 'logradouro', 'numero', 'complemento',
            'bairro', 'cidade', 'estado', 'pais'
        ]
        for field in fields:
            data[field] = self.validated_data.get(field)
        return data

    def save(self, request):
        user = super().save(request)
        for attr, value in self.get_cleaned_data().items():
            setattr(user, attr, value)
        user.save()
        return user


class LoginSerializer(BaseLoginSerializer):
    """Customização futura do login. Por ora, herda tudo direto."""
    pass


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'nome', 'sexo', 'data_nascimento', 'telefone', 'cpf',
            'cep', 'logradouro', 'numero', 'complemento',
            'bairro', 'cidade', 'estado', 'pais', 'date_joined'
        ]
        read_only_fields = ['id', 'email', 'date_joined']


class UsuarioSerializer(serializers.ModelSerializer):
    perfil = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'nome', 'perfil']

    def get_perfil(self, obj):
        if hasattr(obj, 'medico'):
            return 'medico'
        elif hasattr(obj, 'paciente'):
            return 'paciente'
        elif hasattr(obj, 'colaborador'):
            return 'colaborador'
        return 'desconhecido'


class ConsultaResumoSerializer(serializers.ModelSerializer):
    medico_nome = serializers.SerializerMethodField()
    data = serializers.DateTimeField(source='data_hora', format='%d/%m/%Y %H:%M')

    class Meta:
        model = Consulta
        fields = ['id', 'data', 'status', 'tipo', 'is_telemedicina', 'link_telemedicina', 'medico_nome']

    def get_medico_nome(self, obj):
        if obj.medico:
            return obj.medico.get_full_name()
        return "Médico indefinido"
