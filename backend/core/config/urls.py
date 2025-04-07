# core/urls.py

from django.contrib import admin
from django.urls import path, include
from users.views import CustomRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth e usuários
    path('api/users/', include('users.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', CustomRegisterView.as_view(), name="custom_register"),

    # APIs principais
    path('api/epione/', include('epione.urls')),
    path('api/consultas/', include('consultas.urls')),
    path("api/atendimento/", include("atendimento.urls")),
    path("api/fichamedica/", include("fichamedica.urls")),
]
