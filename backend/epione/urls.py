from django.urls import path
from epione.views.epione_aio_views import EpioneAllView
from epione.views.dra_views import DiagnosticoIAView
from epione.views import (
    DoencaListView, SintomaListView, 
    DoencaDetailView, SintomaDetailView
)


urlpatterns = [
    path('sintomas/', SintomaListView.as_view(), name='sintoma-list'),
    path('sintomas/<int:pk>/', SintomaDetailView.as_view(), name='sintoma-detail'),
    path('doencas/', DoencaListView.as_view(), name='doenca-list'),
    path('doencas/<int:pk>/', DoencaDetailView.as_view(), name='doenca-detail'),
    path("epione/all/", EpioneAllView.as_view(), name="epione-all"),
    path("diagnostico/", DiagnosticoIAView.as_view(), name="ia-diagnostico"),
]
