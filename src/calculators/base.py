"""
Clase base para calculadoras de costo de personal
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime


class PayrollCalculator(ABC):
    """Clase base abstracta para calculadoras de nómina por país"""

    def __init__(self, salario_base: float, periodo: str = "mensual"):
        """
        Inicializa la calculadora

        Args:
            salario_base: Salario base del empleado
            periodo: Período de cálculo (mensual, anual)
        """
        self.salario_base = salario_base
        self.periodo = periodo
        self.fecha_calculo = datetime.now()

    @abstractmethod
    def calcular_cargas_sociales(self) -> Dict[str, float]:
        """Calcula las cargas sociales según la legislación del país"""
        pass

    @abstractmethod
    def calcular_beneficios(self) -> Dict[str, float]:
        """Calcula los beneficios laborales según la legislación del país"""
        pass

    @abstractmethod
    def calcular_costo_total(self) -> Dict[str, Any]:
        """Calcula el costo total del empleado"""
        pass

    def _anualizar_si_necesario(self, monto: float) -> float:
        """Convierte un monto mensual a anual si es necesario"""
        if self.periodo == "anual":
            return monto * 12
        return monto

    def get_resumen(self) -> Dict[str, Any]:
        """Obtiene un resumen del cálculo de costos"""
        costo_total = self.calcular_costo_total()

        return {
            'fecha_calculo': self.fecha_calculo.isoformat(),
            'periodo': self.periodo,
            'salario_base': self.salario_base,
            'costo_total': costo_total['total'],
            'desglose': costo_total
        }
