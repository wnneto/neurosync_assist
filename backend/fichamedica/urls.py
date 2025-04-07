from django.urls import path
from fichamedica.views import (
    DadosMedicosView,
    AnamneseView,
    ExameListCreateView,
    ExameDeleteView
)

urlpatterns = [
    path('dados-medicos/', DadosMedicosView.as_view(), name='dados_medicos'),
    path('anamnese/', AnamneseView.as_view(), name='anamnese'),
    path('exames/', ExameListCreateView.as_view(), name='exame-list-create'),
    path('exames/<int:pk>/delete/', ExameDeleteView.as_view(), name='exame-delete'),
]
