from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superusuário precisa ter is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superusuário precisa ter is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')]
    GRUPO_CHOICES = [
        ('paciente', 'Paciente'),
        ('medico', 'Médico'),
        ('colaborador', 'Colaborador')
    ]
    data_nascimento = models.DateField()  # Armazena como YYYY-MM-DD no banco
    
    def get_data_nascimento_br(self):
        """Método helper para exibir no formato BR"""
        return self.data_nascimento.strftime('%d/%m/%Y') if self.data_nascimento else None
    email = models.EmailField('email address', unique=True)
    nome = models.CharField(max_length=150)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    pais = models.CharField(max_length=100, default='Brasil')
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)

    grupo = models.CharField(max_length=20, choices=GRUPO_CHOICES, default='paciente')

    is_active = models.BooleanField(_('ativo'), default=True)
    is_staff = models.BooleanField(_('equipe'), default=False)
    date_joined = models.DateTimeField(_('data de cadastro'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.cpf = self.format_cpf(self.cpf)
        self.telefone = self.format_phone(self.telefone)
        self.cep = self.format_cep(self.cep)
        super().save(*args, **kwargs)

        # Sincroniza com Group do Django
        if self.grupo:
            grupo_obj, _ = Group.objects.get_or_create(name=self.grupo)
            self.groups.set([grupo_obj])

    @staticmethod
    def format_cpf(value):
        digits = ''.join(filter(str.isdigit, value))
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}" if len(digits) == 11 else value

    @staticmethod
    def format_phone(value):
        digits = ''.join(filter(str.isdigit, value))
        return f"+{digits[0:2]} ({digits[2:4]}) {digits[4:9]}-{digits[9:]}" if len(digits) >= 11 else value

    @staticmethod
    def format_cep(value):
        digits = ''.join(filter(str.isdigit, value))
        return f"{digits[:5]}-{digits[5:]}" if len(digits) == 8 else value
