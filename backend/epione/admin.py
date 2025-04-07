from django.contrib import admin
from .models import Doenca, Sintoma, FatorClimatico

admin.site.register(Doenca)
admin.site.register(Sintoma)
admin.site.register(FatorClimatico)
