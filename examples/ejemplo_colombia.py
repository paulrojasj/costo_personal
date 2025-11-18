"""
Ejemplo de uso de la calculadora de costos para Colombia
"""

import sys
sys.path.append('..')

from src.calculators.colombia import ColombiaPayrollCalculator
from src.reports.generator import ReportGenerator


def ejemplo_basico():
    """Ejemplo básico de cálculo para Colombia"""
    print("\n" + "=" * 70)
    print("EJEMPLO 1: Cálculo básico para empleado en Colombia")
    print("=" * 70)

    # Crear calculadora para empleado con salario de $2,500,000 COP
    calc = ColombiaPayrollCalculator(
        salario_base=2500000,
        periodo='mensual',
        nivel_arl=1  # Riesgo mínimo
    )

    # Generar reporte
    generador = ReportGenerator(calc)
    print(generador.generar_reporte_individual(calc))

    # Mostrar métricas
    metricas = calc.get_metricas()
    print("Métricas adicionales:")
    for key, value in metricas.items():
        print(f"  {key}: {value}")


def ejemplo_con_auxilio_transporte():
    """Ejemplo con empleado que recibe auxilio de transporte"""
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Empleado con auxilio de transporte")
    print("=" * 70)

    # Salario menor a 2 SMMLV (recibe auxilio de transporte)
    calc = ColombiaPayrollCalculator(
        salario_base=1500000,
        periodo='mensual',
        nivel_arl=1
    )

    generador = ReportGenerator(calc)
    print(generador.generar_reporte_individual(calc))

    print(f"\nAplica auxilio de transporte: {calc.aplica_auxilio_transporte()}")


def ejemplo_diferentes_niveles_arl():
    """Ejemplo con diferentes niveles de riesgo ARL"""
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Comparación de niveles de riesgo ARL")
    print("=" * 70)

    salario = 3000000

    for nivel in range(1, 6):
        print(f"\n--- Nivel de Riesgo ARL: {nivel} ---")
        calc = ColombiaPayrollCalculator(
            salario_base=salario,
            periodo='mensual',
            nivel_arl=nivel
        )

        costo = calc.calcular_costo_total()
        cargas = costo['cargas_sociales']

        print(f"Salario base:    ${salario:,.0f}")
        print(f"ARL:             ${cargas['arl']:,.0f} ({calc.tasa_arl * 100:.3f}%)")
        print(f"Costo total:     ${costo['costo_mensual']:,.0f}")
        print(f"Ratio:           {costo['ratio_costo_salario']:.2f}x")


def ejemplo_multiple():
    """Ejemplo con múltiples empleados"""
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Análisis de múltiples empleados")
    print("=" * 70)

    # Crear varios empleados con diferentes características
    empleados = [
        ColombiaPayrollCalculator(salario_base=1500000, nivel_arl=1),  # Con aux. transporte
        ColombiaPayrollCalculator(salario_base=2500000, nivel_arl=2),
        ColombiaPayrollCalculator(salario_base=4000000, nivel_arl=1),
        ColombiaPayrollCalculator(salario_base=6000000, nivel_arl=3)
    ]

    # Generar resumen ejecutivo
    generador = ReportGenerator(empleados)
    print(generador.generar_resumen_ejecutivo())


def ejemplo_exportar_json():
    """Ejemplo de exportación a JSON"""
    print("\n" + "=" * 70)
    print("EJEMPLO 5: Exportar datos a JSON")
    print("=" * 70)

    calc = ColombiaPayrollCalculator(
        salario_base=3500000,
        periodo='mensual',
        nivel_arl=2
    )

    generador = ReportGenerator(calc)
    datos = generador.exportar_json('reporte_colombia.json')

    print("Datos exportados a 'reporte_colombia.json'")
    print("\nVista previa:")
    import json
    print(json.dumps(datos, indent=2, ensure_ascii=False))


def ejemplo_comparacion_salarios():
    """Ejemplo comparando diferentes rangos salariales"""
    print("\n" + "=" * 70)
    print("EJEMPLO 6: Comparación de diferentes rangos salariales")
    print("=" * 70)

    salarios = [1300000, 2000000, 3000000, 5000000, 8000000]

    print(f"\n{'Salario Base':>15} | {'Costo Mensual':>15} | {'Ratio':>8} | {'Incremento':>12}")
    print("-" * 70)

    for salario in salarios:
        calc = ColombiaPayrollCalculator(
            salario_base=salario,
            periodo='mensual',
            nivel_arl=1
        )

        costo = calc.calcular_costo_total()
        metricas = calc.get_metricas()

        print(
            f"${salario:>14,} | "
            f"${costo['costo_mensual']:>14,.0f} | "
            f"{costo['ratio_costo_salario']:>8.2f}x | "
            f"{metricas['incremento_porcentual']:>12}"
        )


if __name__ == "__main__":
    # Ejecutar todos los ejemplos
    ejemplo_basico()
    ejemplo_con_auxilio_transporte()
    ejemplo_diferentes_niveles_arl()
    ejemplo_multiple()
    ejemplo_exportar_json()
    ejemplo_comparacion_salarios()

    print("\n" + "=" * 70)
    print("Ejemplos completados exitosamente")
    print("=" * 70)
