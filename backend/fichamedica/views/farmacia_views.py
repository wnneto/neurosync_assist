from rest_framework import generics
from fichamedica.serializers.farmacia_serializers import MedicamentoSerializer
from fichamedica.models.farmacia import Medicamento


class MedicamentoListView(generics.ListCreateAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


class MedicamentoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer