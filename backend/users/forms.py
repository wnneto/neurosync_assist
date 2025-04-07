from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    endereco = forms.CharField(label=_('Endereço'), required=False)
    password1 = forms.CharField(label=_('Senha'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirmação de senha'), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        # Removemos 'endereco' daqui, pois ele não existe no modelo
        fields = ('email', 'nome', 'sexo', 'telefone', 'cpf')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("As senhas não coincidem"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # Se necessário, o campo 'endereco' pode ser tratado aqui, por exemplo:
        # endereco = self.cleaned_data.get('endereco')
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    endereco = forms.CharField(label=_('Endereço'), required=False)
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        # Removemos 'endereco' dos fields para não referenciar um campo inexistente no modelo
        fields = ('email', 'password', 'nome', 'sexo', 'telefone', 'cpf', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]

class CustomSignupForm(forms.Form):
    email = forms.EmailField(label=_('Email'))
    nome = forms.CharField(label=_('Nome completo'))
    cpf = forms.CharField(label=_('CPF'))
    endereco = forms.CharField(label=_('Endereço'), required=False)
    password1 = forms.CharField(label=_('Senha'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirmar senha'), widget=forms.PasswordInput)

    def signup(self, request, user):
        user.nome = self.cleaned_data['nome']
        user.cpf = self.cleaned_data['cpf']
        # Trate o 'endereco' aqui se precisar, salvando em outro lugar ou no perfil do usuário.
        user.save()
