from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class DoencaCronica(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Alergia(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome
    

    CATEGORIAS = [
        ('comportamental', 'Comportamental'),
        ('biologico', 'Biológico'),
        ('ambiental', 'Ambiental'),
        ('psicossocial', 'Psicossocial')
    ]

    FATORES = [
        # Biológicos
        ('obesidade', 'Obesidade (IMC ≥30)'),
        ('hipertensao', 'Hipertensão não controlada'),
        ('dislipidemia', 'Dislipidemia'),
        
        # Comportamentais
        ('tabagismo', 'Tabagismo atual'),
        ('etilismo', 'Consumo de álcool de risco'),
        ('sedentarismo', 'Sedentarismo (<150min/semana)'),
        ('dieta_irregular', 'Dieta inadequada'),
        
        # Psicossociais
        ('estresse_cronico', 'Estresse crônico'),
        ('depressao', 'Episódio depressivo'),
        ('ansiedade', 'Transtorno de ansiedade'),
        
        # Ambientais
        ('poluicao_ar', 'Exposição à poluição atmosférica'),
        ('turnos_noturnos', 'Trabalho em turnos noturnos')
    ]

    categoria = models.CharField(
        max_length=15,
        choices=CATEGORIAS,
        verbose_name="Categoria do Risco"
    )
    
    fator = models.CharField(
        max_length=20,
        choices=FATORES,
        verbose_name="Fator de Risco",
        help_text="Fatores modificáveis com impacto comprovado na morbimortalidade"
    )
    
    severidade = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        verbose_name="Nível de Risco",
        choices=[(1, 'Leve'), (2, 'Moderado'), (3, 'Grave')]
    )
    
    data_identificacao = models.DateField(
        default=timezone.now,
        verbose_name="Data de Identificação"
    )

    class Meta:
        verbose_name = "Fator de Risco Cardiovascular"
        verbose_name_plural = "Estratificação de Risco"
        ordering = ['-severidade', 'categoria']
        indexes = [
            models.Index(fields=['fator', 'severidade']),
        ]

    def __str__(self):
        return f"{self.get_fator_display()} ({self.get_severidade_display()})"

class FatorClimatico(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    TIPO_CLIMA_CHOICES = [
        ("equatorial", "Equatorial"),
        ("tropical", "Tropical"),
        ("temperado", "Temperado"),
        ("subtropical", "Subtropical"),
        ("semiárido", "Semiárido"),
        ("árido", "Árido"),
        ("mediterrâneo", "Mediterrâneo"),
        ("alpino", "Alpino"),
        ("polar", "Polar"),
    ]
    tipo = models.CharField(
        max_length=50,
        choices=TIPO_CLIMA_CHOICES,
        default="temperado"
    )
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome