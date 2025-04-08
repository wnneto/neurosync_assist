from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser
from django.utils.formats import date_format


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('email', 'nome', 'cpf', 'telefone', 'grupo', 'is_staff', 'is_active', "aceitou_termos", 'format_date_joined')
    list_filter = ('is_staff', 'is_active', 'sexo', 'grupo')
    search_fields = ('email', 'cpf', 'nome')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {
            'fields': (
                'nome', 'sexo', 'data_nascimento',
                'telefone', 'cpf',
                'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'pais'
            )
        }),
        ('Permissões', {'fields': ('grupo', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas', {'fields': ('last_login', 'date_joined')}),
        ("Aceite Legal", {
            "fields": ("aceitou_termos", "data_aceite_termo", "versao_termo")
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "email", "password1", "password2", 
                "nome", "sexo", "cpf", "is_active", 
                "is_staff", "is_superuser"
            ),
        }),
    )

    readonly_fields = ('last_login', 'date_joined')

    def format_date_joined(self, obj):
        return date_format(obj.date_joined, format='d-m-Y')
    format_date_joined.short_description = 'Data de Cadastro'
