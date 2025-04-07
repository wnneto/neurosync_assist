from django.urls import path
from atendimento.views.consulta_view import AtendimentoCreateView
from atendimento.views.documento_view import DocumentoConsultaCreateView
from atendimento.views.iniciar_telemedicina_view import IniciarTelemedicinaView

urlpatterns = [
    path('registrar/', AtendimentoCreateView.as_view(), name='registrar-atendimento'),
    path('documento/', DocumentoConsultaCreateView.as_view(), name='criar-documento'),
    path('consulta/<int:consulta_id>/iniciar-telemedicina/', IniciarTelemedicinaView.as_view()),
]
