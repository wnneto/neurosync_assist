from rest_framework import generics
from epione.models.doenca import Doenca
from epione.serializers.doenca_serializer import DoencaSerializer


class DoencaListView(generics.ListCreateAPIView):
    queryset = Doenca.objects.all()
    serializer_class = DoencaSerializer

class DoencaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doenca.objects.all()
    serializer_class = DoencaSerializer
