from rest_framework import generics
from fichamedica.models.estrutura import Doenca, Sintoma
from fichamedica.serializers.estrutura_serializers import DoencaSerializer, SintomaSerializer



class DoencaListView(generics.ListCreateAPIView):
    queryset = Doenca.objects.all()
    serializer_class = DoencaSerializer

class DoencaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doenca.objects.all()
    serializer_class = DoencaSerializer


class SintomaListView(generics.ListCreateAPIView):
    queryset = Sintoma.objects.all()
    serializer_class = SintomaSerializer

class SintomaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sintoma.objects.all()
    serializer_class = SintomaSerializer
