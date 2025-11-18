#!/usr/bin/env python3
"""
Ejemplo rápido de uso del sistema de costo de personal
"""

from src.calculators.peru import PeruPayrollCalculator
from src.calculators.colombia import ColombiaPayrollCalculator
from src.reports.generator import ReportGenerator


def main():
    print("=" * 70)
    print("SISTEMA DE CÁLCULO DE COSTO DE PERSONAL")
    print("=" * 70)
    print()

    # EJEMPLO PERÚ
    print("1. CÁLCULO PARA PERÚ")
    print("-" * 70)

    empleado_pe = PeruPayrollCalculator(
        salario_base=4000,
        tiene_hijos=True
    )

    costo_pe = empleado_pe.calcular_costo_total()
    print(f"Salario base:       S/ {costo_pe['salario_base']:,.2f}")
    print(f"Costo mensual:      S/ {costo_pe['costo_mensual']:,.2f}")
    print(f"Costo anual:        S/ {costo_pe['costo_anual']:,.2f}")
    print(f"Ratio costo/salario: {costo_pe['ratio_costo_salario']}x")
    print()

    # EJEMPLO COLOMBIA
    print("2. CÁLCULO PARA COLOMBIA")
    print("-" * 70)

    empleado_co = ColombiaPayrollCalculator(
        salario_base=3500000,
        nivel_arl=1
    )

    costo_co = empleado_co.calcular_costo_total()
    print(f"Salario base:       $ {costo_co['salario_base']:,.0f}")
    print(f"Costo mensual:      $ {costo_co['costo_mensual']:,.0f}")
    print(f"Costo anual:        $ {costo_co['costo_anual']:,.0f}")
    print(f"Ratio costo/salario: {costo_co['ratio_costo_salario']}x")
    print()

    # REPORTE COMPARATIVO
    print("3. COMPARACIÓN PE vs CO")
    print("-" * 70)

    generador = ReportGenerator([empleado_pe, empleado_co])
    print(generador.generar_reporte_comparativo())


if __name__ == "__main__":
    main()
