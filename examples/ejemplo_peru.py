"""
Ejemplo de uso de la calculadora de costos para Perú
"""

import sys
sys.path.append('..')

from src.calculators.peru import PeruPayrollCalculator
from src.reports.generator import ReportGenerator


def ejemplo_basico():
    """Ejemplo básico de cálculo para Perú"""
    print("\n" + "=" * 70)
    print("EJEMPLO 1: Cálculo básico para empleado en Perú")
    print("=" * 70)

    # Crear calculadora para empleado con salario de S/ 3,000
    calc = PeruPayrollCalculator(
        salario_base=3000,
        periodo='mensual',
        tiene_hijos=False,
        incluye_sctr=False
    )

    # Generar reporte
    generador = ReportGenerator(calc)
    print(generador.generar_reporte_individual(calc))

    # Mostrar métricas
    metricas = calc.get_metricas()
    print("Métricas adicionales:")
    for key, value in metricas.items():
        print(f"  {key}: {value}")


def ejemplo_con_asignacion_familiar():
    """Ejemplo con empleado que tiene hijos (asignación familiar)"""
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Empleado con asignación familiar")
    print("=" * 70)

    calc = PeruPayrollCalculator(
        salario_base=4500,
        periodo='mensual',
        tiene_hijos=True,  # Tiene hijos
        incluye_sctr=False
    )

    generador = ReportGenerator(calc)
    print(generador.generar_reporte_individual(calc))


def ejemplo_con_sctr():
    """Ejemplo con empleado en trabajo de riesgo (incluye SCTR)"""
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Empleado con SCTR (trabajo de riesgo)")
    print("=" * 70)

    calc = PeruPayrollCalculator(
        salario_base=5000,
        periodo='mensual',
        tiene_hijos=True,
        incluye_sctr=True  # Incluye SCTR
    )

    generador = ReportGenerator(calc)
    print(generador.generar_reporte_individual(calc))


def ejemplo_multiple():
    """Ejemplo con múltiples empleados"""
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Análisis de múltiples empleados")
    print("=" * 70)

    # Crear varios empleados
    empleados = [
        PeruPayrollCalculator(salario_base=3000, tiene_hijos=False),
        PeruPayrollCalculator(salario_base=4500, tiene_hijos=True),
        PeruPayrollCalculator(salario_base=6000, tiene_hijos=False, incluye_sctr=True),
        PeruPayrollCalculator(salario_base=8000, tiene_hijos=True)
    ]

    # Generar resumen ejecutivo
    generador = ReportGenerator(empleados)
    print(generador.generar_resumen_ejecutivo())


def ejemplo_exportar_json():
    """Ejemplo de exportación a JSON"""
    print("\n" + "=" * 70)
    print("EJEMPLO 5: Exportar datos a JSON")
    print("=" * 70)

    calc = PeruPayrollCalculator(
        salario_base=5000,
        periodo='mensual',
        tiene_hijos=True
    )

    generador = ReportGenerator(calc)
    datos = generador.exportar_json('reporte_peru.json')

    print("Datos exportados a 'reporte_peru.json'")
    print("\nVista previa:")
    import json
    print(json.dumps(datos, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    # Ejecutar todos los ejemplos
    ejemplo_basico()
    ejemplo_con_asignacion_familiar()
    ejemplo_con_sctr()
    ejemplo_multiple()
    ejemplo_exportar_json()

    print("\n" + "=" * 70)
    print("Ejemplos completados exitosamente")
    print("=" * 70)
