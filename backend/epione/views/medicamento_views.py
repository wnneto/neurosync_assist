# epione/views/medicamento_view.py
from rest_framework import generics
from epione.models.medicamento import Medicamento
from epione.serializers.medicamento_serializer import MedicamentoSerializer


class MedicamentoListView(generics.ListCreateAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


class MedicamentoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
