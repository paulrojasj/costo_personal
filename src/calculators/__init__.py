"""
Módulo de calculadoras de costo de personal por país
"""

from .peru import PeruPayrollCalculator
from .colombia import ColombiaPayrollCalculator

__all__ = ['PeruPayrollCalculator', 'ColombiaPayrollCalculator']
