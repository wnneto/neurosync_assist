from django.contrib import admin
from .models import (
    # Referências
    DoencaCronica, Alergia, TipoMedicamento, Medicamento,
    # Dados clínicos
    DadosMedicos, HistoricoFamiliar, Anamnese,
    # Documentos
    Cirurgia, Exame
)


# ==============================
# Referências
# ==============================

@admin.register(DoencaCronica)
class DoencaCronicaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Alergia)
class AlergiaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(TipoMedicamento)
class TipoMedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nome',)


# ==============================
# Dados Médicos
# ==============================

@admin.register(DadosMedicos)
class DadosMedicosAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'get_alergias', 'get_doencas', 'get_medicamentos')
    search_fields = ('usuario__nome', 'usuario__email')

    def get_alergias(self, obj):
        return ", ".join([a.nome for a in obj.alergias.all()])
    get_alergias.short_description = 'Alergias'

    def get_doencas(self, obj):
        return ", ".join([d.nome for d in obj.doencas_cronicas.all()])
    get_doencas.short_description = 'Doenças Crônicas'

    def get_medicamentos(self, obj):
        return ", ".join([m.nome for m in obj.medicamentos_em_uso.all()])
    get_medicamentos.short_description = 'Medicamentos em uso'


@admin.register(HistoricoFamiliar)
class HistoricoFamiliarAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'doenca', 'parentesco')
    list_filter = ('parentesco',)
    search_fields = ('usuario__nome', 'doenca__nome')


@admin.register(Anamnese)
class AnamneseAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'periodo', 'updated_at')
    search_fields = ('usuario__nome',)
    readonly_fields = ('updated_at',)


# ==============================
# Documentos
# ==============================

@admin.register(Cirurgia)
class CirurgiaAdmin(admin.ModelAdmin):
    list_display = ('dados_medicos', 'categoria', 'periodo')
    list_filter = ('categoria', 'periodo')
    search_fields = ('dados_medicos__usuario__nome',)


@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'periodo')
    list_filter = ('tipo', 'periodo')
    search_fields = ('usuario__nome',)
