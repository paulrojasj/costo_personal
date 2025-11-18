"""
Calculadora de costo de personal para Colombia (CO)
Basado en la legislación laboral colombiana
"""

from typing import Dict, Any
from .base import PayrollCalculator


class ColombiaPayrollCalculator(PayrollCalculator):
    """
    Calculadora de costos laborales para Colombia

    Incluye:
    - Salud (8.5%)
    - Pensión (12%)
    - ARL (Riesgos Laborales)
    - Caja de Compensación (4%)
    - ICBF (3%)
    - SENA (2%)
    - Prima de servicios
    - Cesantías
    - Intereses sobre cesantías
    - Vacaciones
    - Auxilio de transporte
    """

    # Tasas según legislación colombiana 2024
    TASA_SALUD = 0.085  # 8.5%
    TASA_PENSION = 0.12  # 12%
    TASA_ARL_NIVEL_I = 0.00522  # 0.522% (Nivel I - riesgo mínimo)
    TASA_CAJA_COMPENSACION = 0.04  # 4%
    TASA_ICBF = 0.03  # 3%
    TASA_SENA = 0.02  # 2%
    TASA_INTERESES_CESANTIAS = 0.12  # 12% anual

    SALARIO_MINIMO = 1300000  # $1,300,000 COP (2024)
    AUXILIO_TRANSPORTE = 162000  # $162,000 COP (2024)
    LIMITE_AUXILIO_TRANSPORTE = SALARIO_MINIMO * 2  # 2 SMMLV

    def __init__(self, salario_base: float, periodo: str = "mensual",
                 nivel_arl: int = 1):
        """
        Inicializa calculadora para Colombia

        Args:
            salario_base: Salario base mensual en pesos colombianos
            periodo: 'mensual' o 'anual'
            nivel_arl: Nivel de riesgo ARL (1-5), default 1
        """
        super().__init__(salario_base, periodo)
        self.nivel_arl = nivel_arl
        self.tasa_arl = self._obtener_tasa_arl(nivel_arl)

    def _obtener_tasa_arl(self, nivel: int) -> float:
        """Obtiene la tasa de ARL según el nivel de riesgo"""
        tasas = {
            1: 0.00522,  # 0.522%
            2: 0.01044,  # 1.044%
            3: 0.02436,  # 2.436%
            4: 0.04350,  # 4.35%
            5: 0.06960   # 6.96%
        }
        return tasas.get(nivel, tasas[1])

    def aplica_auxilio_transporte(self) -> bool:
        """Verifica si el empleado tiene derecho a auxilio de transporte"""
        return self.salario_base <= self.LIMITE_AUXILIO_TRANSPORTE

    def calcular_cargas_sociales(self) -> Dict[str, float]:
        """
        Calcula las cargas sociales del empleador en Colombia

        Returns:
            Diccionario con el desglose de cargas sociales (parafiscales)
        """
        cargas = {}

        # Salud: 8.5% del salario base
        cargas['salud'] = self.salario_base * self.TASA_SALUD

        # Pensión: 12% del salario base
        cargas['pension'] = self.salario_base * self.TASA_PENSION

        # ARL según nivel de riesgo
        cargas['arl'] = self.salario_base * self.tasa_arl
        cargas['arl_nivel'] = self.nivel_arl

        # Caja de Compensación: 4%
        cargas['caja_compensacion'] = self.salario_base * self.TASA_CAJA_COMPENSACION

        # ICBF: 3%
        cargas['icbf'] = self.salario_base * self.TASA_ICBF

        # SENA: 2%
        cargas['sena'] = self.salario_base * self.TASA_SENA

        # Total cargas sociales
        cargas['total_cargas'] = (
            cargas['salud'] +
            cargas['pension'] +
            cargas['arl'] +
            cargas['caja_compensacion'] +
            cargas['icbf'] +
            cargas['sena']
        )

        # Porcentaje total
        cargas['porcentaje_total'] = round((cargas['total_cargas'] / self.salario_base) * 100, 2)

        return cargas

    def calcular_beneficios(self) -> Dict[str, float]:
        """
        Calcula los beneficios laborales en Colombia

        Returns:
            Diccionario con el desglose de beneficios (prestaciones sociales)
        """
        beneficios = {}

        # Auxilio de transporte (si aplica)
        if self.aplica_auxilio_transporte():
            beneficios['auxilio_transporte'] = self.AUXILIO_TRANSPORTE
        else:
            beneficios['auxilio_transporte'] = 0

        # Base para cálculo de prestaciones (incluye auxilio de transporte para algunos conceptos)
        base_prestaciones = self.salario_base

        # Prima de servicios: 1 salario al año (se paga en 2 partes: jun-jul)
        # Base: (Salario + Auxilio transporte) * días trabajados / 360
        prima_anual = base_prestaciones + beneficios['auxilio_transporte']
        beneficios['prima_servicios_anual'] = prima_anual
        beneficios['prima_servicios_mensual'] = prima_anual / 12

        # Cesantías: 1 salario al año
        # Base: (Salario + Auxilio transporte) * días trabajados / 360
        cesantias_anual = base_prestaciones + beneficios['auxilio_transporte']
        beneficios['cesantias_anual'] = cesantias_anual
        beneficios['cesantias_mensual'] = cesantias_anual / 12

        # Intereses sobre cesantías: 12% anual sobre las cesantías
        intereses_cesantias_anual = cesantias_anual * self.TASA_INTERESES_CESANTIAS
        beneficios['intereses_cesantias_anual'] = intereses_cesantias_anual
        beneficios['intereses_cesantias_mensual'] = intereses_cesantias_anual / 12

        # Vacaciones: 15 días hábiles al año
        # Se calculan sobre el salario base únicamente (sin auxilio de transporte)
        vacaciones_anual = self.salario_base / 2  # 15 días = 0.5 meses
        beneficios['vacaciones_anual'] = vacaciones_anual
        beneficios['vacaciones_mensual'] = vacaciones_anual / 12

        return beneficios

    def calcular_costo_total(self) -> Dict[str, Any]:
        """
        Calcula el costo total del empleado para el empleador

        Returns:
            Diccionario con el desglose completo de costos
        """
        cargas = self.calcular_cargas_sociales()
        beneficios = self.calcular_beneficios()

        # Costo mensual base
        costo_mensual_base = self.salario_base

        # Auxilio de transporte mensual
        costo_auxilio_transporte = beneficios['auxilio_transporte']

        # Cargas sociales mensuales (sobre salario base)
        costo_cargas_mensual = cargas['total_cargas']

        # Prestaciones sociales mensuales (prorrateadas)
        costo_prestaciones_mensual = (
            beneficios['prima_servicios_mensual'] +
            beneficios['cesantias_mensual'] +
            beneficios['intereses_cesantias_mensual'] +
            beneficios['vacaciones_mensual']
        )

        # Total mensual
        costo_total_mensual = (
            costo_mensual_base +
            costo_auxilio_transporte +
            costo_cargas_mensual +
            costo_prestaciones_mensual
        )

        resultado = {
            'pais': 'CO',
            'moneda': 'COP',
            'salario_base': self.salario_base,
            'cargas_sociales': cargas,
            'beneficios': beneficios,
            'costo_mensual': costo_total_mensual,
            'costo_anual': costo_total_mensual * 12,
            'desglose_mensual': {
                'salario_base': costo_mensual_base,
                'auxilio_transporte': costo_auxilio_transporte,
                'cargas_sociales': costo_cargas_mensual,
                'prestaciones_prorrateadas': costo_prestaciones_mensual,
                'total': costo_total_mensual
            },
            'ratio_costo_salario': round(costo_total_mensual / self.salario_base, 2),
            'total': costo_total_mensual if self.periodo == 'mensual' else costo_total_mensual * 12
        }

        return resultado

    def get_metricas(self) -> Dict[str, Any]:
        """Obtiene métricas clave del costo de personal"""
        costo = self.calcular_costo_total()

        return {
            'costo_efectivo_vs_salario': f"{costo['ratio_costo_salario']}x",
            'incremento_porcentual': f"{round((costo['ratio_costo_salario'] - 1) * 100, 2)}%",
            'costo_adicional_mensual': round(costo['costo_mensual'] - self.salario_base, 2),
            'proyeccion_anual': round(costo['costo_anual'], 2),
            'nivel_riesgo_arl': self.nivel_arl,
            'aplica_auxilio_transporte': self.aplica_auxilio_transporte()
        }
