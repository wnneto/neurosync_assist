from django.urls import path
from users.views.profile_views import PacienteCompletoView
from users.views.colaborador_views import ListaUsuariosView
from users.views import (
    CustomRegisterView, CustomLoginView,
    UserProfileView,
)

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='custom_register'),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('admin/usuarios/', ListaUsuariosView.as_view(), name='lista-usuarios'),
    path("paciente/<int:paciente_id>/completo/", PacienteCompletoView.as_view()),
]
