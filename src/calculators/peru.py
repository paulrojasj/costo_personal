"""
Calculadora de costo de personal para Perú (PE)
Basado en la legislación laboral peruana
"""

from typing import Dict, Any
from .base import PayrollCalculator


class PeruPayrollCalculator(PayrollCalculator):
    """
    Calculadora de costos laborales para Perú

    Incluye:
    - EsSalud (9%)
    - AFP/ONP (variable, default 13%)
    - Gratificaciones (2 al año)
    - CTS (Compensación por Tiempo de Servicios)
    - Vacaciones
    - Asignación familiar (opcional)
    """

    # Tasas según legislación peruana 2024
    TASA_ESSALUD = 0.09  # 9%
    TASA_AFP_EMPLEADOR = 0.0013  # Seguro: 0.13% aprox
    TASA_SCTR = 0.0063  # Promedio SCTR: 0.63%
    SALARIO_MINIMO = 1025  # S/ 1,025 (2024)
    TASA_ASIGNACION_FAMILIAR = 0.10  # 10% del salario mínimo

    def __init__(self, salario_base: float, periodo: str = "mensual",
                 tiene_hijos: bool = False, incluye_sctr: bool = False,
                 tasa_afp: float = 0.13):
        """
        Inicializa calculadora para Perú

        Args:
            salario_base: Salario base mensual en soles
            periodo: 'mensual' o 'anual'
            tiene_hijos: Si tiene hijos (para asignación familiar)
            incluye_sctr: Si incluye Seguro Complementario de Trabajo de Riesgo
            tasa_afp: Tasa de AFP del empleador (default 13%)
        """
        super().__init__(salario_base, periodo)
        self.tiene_hijos = tiene_hijos
        self.incluye_sctr = incluye_sctr
        self.tasa_afp = tasa_afp

    def calcular_cargas_sociales(self) -> Dict[str, float]:
        """
        Calcula las cargas sociales del empleador en Perú

        Returns:
            Diccionario con el desglose de cargas sociales
        """
        cargas = {}

        # EsSalud: 9% del salario bruto
        cargas['essalud'] = self.salario_base * self.TASA_ESSALUD

        # AFP empleador (aportes del empleador)
        cargas['afp_empleador'] = self.salario_base * self.TASA_AFP_EMPLEADOR

        # SCTR si aplica
        if self.incluye_sctr:
            cargas['sctr'] = self.salario_base * self.TASA_SCTR
        else:
            cargas['sctr'] = 0

        cargas['total_cargas'] = sum(cargas.values())

        return cargas

    def calcular_beneficios(self) -> Dict[str, float]:
        """
        Calcula los beneficios laborales en Perú

        Returns:
            Diccionario con el desglose de beneficios
        """
        beneficios = {}

        # Asignación familiar (si tiene hijos)
        if self.tiene_hijos:
            beneficios['asignacion_familiar'] = self.SALARIO_MINIMO * self.TASA_ASIGNACION_FAMILIAR
        else:
            beneficios['asignacion_familiar'] = 0

        # Salario bruto (base + asignación familiar)
        salario_bruto = self.salario_base + beneficios['asignacion_familiar']

        # Gratificaciones: 2 al año (Julio y Diciembre)
        # Cada gratificación es equivalente a 1 salario bruto + 9% EsSalud
        gratificacion_unitaria = salario_bruto * (1 + self.TASA_ESSALUD)
        beneficios['gratificaciones_anual'] = gratificacion_unitaria * 2

        # Prorrateado mensual
        beneficios['gratificaciones_mensual'] = beneficios['gratificaciones_anual'] / 12

        # CTS: 1 salario bruto + 1/6 de gratificaciones al año
        cts_anual = salario_bruto + (beneficios['gratificaciones_anual'] / 6)
        beneficios['cts_anual'] = cts_anual
        beneficios['cts_mensual'] = cts_anual / 12

        # Vacaciones: 30 días al año (equivalente a 1 salario mensual)
        beneficios['vacaciones_anual'] = salario_bruto
        beneficios['vacaciones_mensual'] = salario_bruto / 12

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

        # Cargas sociales mensuales
        costo_cargas_mensual = cargas['total_cargas']

        # Beneficios mensuales (prorrateados)
        costo_beneficios_mensual = (
            beneficios['asignacion_familiar'] +
            beneficios['gratificaciones_mensual'] +
            beneficios['cts_mensual'] +
            beneficios['vacaciones_mensual']
        )

        # Total mensual
        costo_total_mensual = (
            costo_mensual_base +
            costo_cargas_mensual +
            costo_beneficios_mensual
        )

        resultado = {
            'pais': 'PE',
            'moneda': 'PEN',
            'salario_base': self.salario_base,
            'cargas_sociales': cargas,
            'beneficios': beneficios,
            'costo_mensual': costo_total_mensual,
            'costo_anual': costo_total_mensual * 12,
            'desglose_mensual': {
                'salario_base': costo_mensual_base,
                'cargas_sociales': costo_cargas_mensual,
                'beneficios_prorrateados': costo_beneficios_mensual,
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
            'proyeccion_anual': round(costo['costo_anual'], 2)
        }
