
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
    telefone = serializers.CharField(required=True)
    cpf = serializers.CharField(required=True)
    cep = serializers.CharField(required=True)
    logradouro = serializers.CharField(required=True)
    numero = serializers.CharField(required=True)
    complemento = serializers.CharField(required=False, allow_blank=True)
    bairro = serializers.CharField(required=True)
    cidade = serializers.CharField(required=True)
    estado = serializers.CharField(required=True)
    aceitou_termos = serializers.BooleanField(required=True)
    pais = serializers.CharField(required=False, default='Brasil')

    username = None  # remove o campo username

    def validate_nome(self, value):
        return ' '.join(word.capitalize() for word in value.strip().split())

    def validate_data_nascimento(self, value):
        if isinstance(value, str) and '/' in value:
            dia, mes, ano = value.split('/')
            return f'{ano}-{mes}-{dia}'
        return value  # Já é datetime.date


    def validate_cpf(self, value):
        cpf_formatado = formatar_cpf(value)
        if not validar_cpf(cpf_formatado):
            raise serializers.ValidationError("CPF inválido.")
        if CustomUser.objects.filter(cpf=cpf_formatado).exists():
            raise serializers.ValidationError("Já existe um usuário com este CPF.")
        return cpf_formatado

    def validate_telefone(self, value):
        return formatar_telefone(value)

    def validate_cep(self, value):
        return formatar_cep(value)

    def validate(self, data):
        endereco = buscar_endereco_por_cep(data.get('cep'))
        if not endereco:
            raise serializers.ValidationError("CEP inválido ou não encontrado.")
        for campo in ['logradouro', 'bairro', 'cidade', 'estado']:
            if not data.get(campo):
                data[campo] = endereco.get(campo, '')
        return data

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        campos_personalizados = [
            'nome', 'sexo', 'data_nascimento', 'telefone', 'cpf',
            'cep', 'logradouro', 'numero', 'complemento',
            'bairro', 'cidade', 'estado', 'pais', 'aceitou_termos'
        ]
        for campo in campos_personalizados:
            data[campo] = self.validated_data.get(campo)
        return data

    def save(self, request):
        cleaned_data = self.get_cleaned_data()

        user = CustomUser.objects.create_user(
            email=cleaned_data['email'],
            password=cleaned_data['password1'],
            nome=cleaned_data['nome'],
            sexo=cleaned_data['sexo'],
            data_nascimento=cleaned_data['data_nascimento'],
            telefone=cleaned_data['telefone'],
            cpf=cleaned_data['cpf'],
            cep=cleaned_data['cep'],
            logradouro=cleaned_data['logradouro'],
            numero=cleaned_data['numero'],
            complemento=cleaned_data.get('complemento', ''),
            bairro=cleaned_data['bairro'],
            cidade=cleaned_data['cidade'],
            estado=cleaned_data['estado'],
            aceitou_termos=cleaned_data['aceitou_termos'],
            versao_termo="1.0",
            pais=cleaned_data.get('pais', 'Brasil'),
        )

        # Importante para integração com allauth
        self.custom_signup(request, user)
        return user


    def create_user_instance(self, request):
        adapter = self.get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        return user


class LoginSerializer(BaseLoginSerializer):
    pass


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'nome', 'sexo', 'data_nascimento', 'telefone', 'cpf',
            'cep', 'logradouro', 'numero', 'complemento',
            'bairro', 'cidade', 'estado', 'pais', 'date_joined', 'data_aceite_termo',
            'versao_termo'
        ]
        read_only_fields = ['id', 'email', 'date_joined', 'data_aceite_termo', 'versao_termo']


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
