from rest_framework import generics
from epione.models.sintoma import Sintoma
from epione.serializers.sintoma_serializer import SintomaSerializer


class SintomaListView(generics.ListCreateAPIView):
    queryset = Sintoma.objects.all()
    serializer_class = SintomaSerializer

class SintomaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sintoma.objects.all()
    serializer_class = SintomaSerializer
