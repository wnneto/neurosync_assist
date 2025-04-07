# epione/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from epione.models import Doenca, Sintoma, FatorClimatico

class EpioneEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Criação inicial de objetos para os testes
        self.doenca1 = Doenca.objects.create(
            nome="Gripe",
            gravidade="leve",
            duracao_media_dias=5
        )
        self.sintoma1 = Sintoma.objects.create(nome="Febre")
        self.clima1 = FatorClimatico.objects.create(nome="Frio")

        self.doenca1.sintomas.add(self.sintoma1)
        self.doenca1.fatores_climaticos.add(self.clima1)

    def test_listar_doencas(self):
        url = reverse('epione:doencas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_listar_sintomas(self):
        url = reverse('epione:sintomas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_listar_fatores_climaticos(self):
        url = reverse('epione:fatores-climaticos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_detalhes_agrupados_epione_info(self):
        url = reverse('epione:info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('doencas', response.data)
        self.assertIn('sintomas', response.data)
        self.assertIn('fatores_climaticos', response.data)
