"""
Ejemplo comparativo entre Perú y Colombia
"""

import sys
sys.path.append('..')

from src.calculators.peru import PeruPayrollCalculator
from src.calculators.colombia import ColombiaPayrollCalculator
from src.reports.generator import ReportGenerator


def comparacion_basica():
    """Comparación básica entre PE y CO"""
    print("\n" + "=" * 70)
    print("COMPARACIÓN PE vs CO - Caso Base")
    print("=" * 70)

    # Perú: S/ 3,000 (aprox USD 800)
    calc_pe = PeruPayrollCalculator(
        salario_base=3000,
        periodo='mensual',
        tiene_hijos=False
    )

    # Colombia: $3,500,000 (aprox USD 875)
    calc_co = ColombiaPayrollCalculator(
        salario_base=3500000,
        periodo='mensual',
        nivel_arl=1
    )

    # Generar reporte comparativo
    generador = ReportGenerator([calc_pe, calc_co])
    print(generador.generar_reporte_comparativo())


def comparacion_detallada():
    """Comparación detallada con múltiples escenarios"""
    print("\n" + "=" * 70)
    print("COMPARACIÓN DETALLADA PE vs CO")
    print("=" * 70)

    print("\nEscenario 1: Salario base sin beneficios adicionales")
    print("-" * 70)

    pe1 = PeruPayrollCalculator(salario_base=3000, tiene_hijos=False)
    co1 = ColombiaPayrollCalculator(salario_base=3500000, nivel_arl=1)

    generador1 = ReportGenerator([pe1, co1])
    print(generador1.generar_reporte_comparativo())

    print("\nEscenario 2: Con beneficios/prestaciones adicionales")
    print("-" * 70)

    pe2 = PeruPayrollCalculator(salario_base=5000, tiene_hijos=True, incluye_sctr=True)
    co2 = ColombiaPayrollCalculator(salario_base=2000000, nivel_arl=3)

    generador2 = ReportGenerator([pe2, co2])
    print(generador2.generar_reporte_comparativo())


def analisis_estructura_costos():
    """Análisis de la estructura de costos en cada país"""
    print("\n" + "=" * 70)
    print("ANÁLISIS DE ESTRUCTURA DE COSTOS")
    print("=" * 70)

    # Perú
    print("\nPERÚ - Estructura de costos:")
    print("-" * 70)

    calc_pe = PeruPayrollCalculator(salario_base=4000, tiene_hijos=True)
    costo_pe = calc_pe.calcular_costo_total()

    print(f"Salario base:               S/ {costo_pe['salario_base']:,.2f}")
    print(f"Cargas sociales:            S/ {costo_pe['cargas_sociales']['total_cargas']:,.2f}")
    print(f"Beneficios (prorrateados):  S/ {costo_pe['desglose_mensual']['beneficios_prorrateados']:,.2f}")
    print(f"TOTAL:                      S/ {costo_pe['costo_mensual']:,.2f}")

    cargas_pe_pct = (costo_pe['cargas_sociales']['total_cargas'] / costo_pe['salario_base']) * 100
    beneficios_pe_pct = (costo_pe['desglose_mensual']['beneficios_prorrateados'] / costo_pe['salario_base']) * 100

    print(f"\nPorcentajes sobre salario base:")
    print(f"  Cargas sociales:    {cargas_pe_pct:.2f}%")
    print(f"  Beneficios:         {beneficios_pe_pct:.2f}%")
    print(f"  Total incremento:   {(costo_pe['ratio_costo_salario'] - 1) * 100:.2f}%")

    # Colombia
    print("\n\nCOLOMBIA - Estructura de costos:")
    print("-" * 70)

    calc_co = ColombiaPayrollCalculator(salario_base=5000000, nivel_arl=2)
    costo_co = calc_co.calcular_costo_total()

    print(f"Salario base:               $ {costo_co['salario_base']:,.0f}")
    print(f"Auxilio de transporte:      $ {costo_co['desglose_mensual']['auxilio_transporte']:,.0f}")
    print(f"Cargas sociales:            $ {costo_co['cargas_sociales']['total_cargas']:,.0f}")
    print(f"Prestaciones (prorrateadas): $ {costo_co['desglose_mensual']['prestaciones_prorrateadas']:,.0f}")
    print(f"TOTAL:                      $ {costo_co['costo_mensual']:,.0f}")

    cargas_co_pct = (costo_co['cargas_sociales']['total_cargas'] / costo_co['salario_base']) * 100
    prestaciones_co_pct = (costo_co['desglose_mensual']['prestaciones_prorrateadas'] / costo_co['salario_base']) * 100

    print(f"\nPorcentajes sobre salario base:")
    print(f"  Cargas sociales:    {cargas_co_pct:.2f}%")
    print(f"  Prestaciones:       {prestaciones_co_pct:.2f}%")
    print(f"  Total incremento:   {(costo_co['ratio_costo_salario'] - 1) * 100:.2f}%")


def comparacion_equipos():
    """Comparación de costos de equipos completos"""
    print("\n" + "=" * 70)
    print("COMPARACIÓN DE COSTOS - EQUIPOS COMPLETOS")
    print("=" * 70)

    # Equipo en Perú
    print("\nEquipo en Perú (5 empleados):")
    equipo_pe = [
        PeruPayrollCalculator(salario_base=2500, tiene_hijos=False),  # Jr Dev
        PeruPayrollCalculator(salario_base=4000, tiene_hijos=True),   # Mid Dev
        PeruPayrollCalculator(salario_base=6000, tiene_hijos=True),   # Sr Dev
        PeruPayrollCalculator(salario_base=8000, tiene_hijos=False),  # Tech Lead
        PeruPayrollCalculator(salario_base=3500, tiene_hijos=True)    # QA
    ]

    # Equipo en Colombia
    print("\nEquipo en Colombia (5 empleados):")
    equipo_co = [
        ColombiaPayrollCalculator(salario_base=2500000, nivel_arl=1),  # Jr Dev
        ColombiaPayrollCalculator(salario_base=4000000, nivel_arl=1),  # Mid Dev
        ColombiaPayrollCalculator(salario_base=7000000, nivel_arl=1),  # Sr Dev
        ColombiaPayrollCalculator(salario_base=10000000, nivel_arl=1), # Tech Lead
        ColombiaPayrollCalculator(salario_base=3500000, nivel_arl=1)   # QA
    ]

    # Generar reportes
    gen_pe = ReportGenerator(equipo_pe)
    gen_co = ReportGenerator(equipo_co)

    print("\n--- RESUMEN PERÚ ---")
    print(gen_pe.generar_resumen_ejecutivo())

    print("\n--- RESUMEN COLOMBIA ---")
    print(gen_co.generar_resumen_ejecutivo())


def exportar_comparacion_completa():
    """Exporta comparación completa a JSON"""
    print("\n" + "=" * 70)
    print("EXPORTAR COMPARACIÓN COMPLETA")
    print("=" * 70)

    # Crear calculadoras para ambos países
    calc_pe = PeruPayrollCalculator(salario_base=5000, tiene_hijos=True)
    calc_co = ColombiaPayrollCalculator(salario_base=6000000, nivel_arl=2)

    # Exportar
    generador = ReportGenerator([calc_pe, calc_co])
    datos = generador.exportar_json('comparacion_pe_co.json')

    print("Comparación exportada a 'comparacion_pe_co.json'")
    print("\nResumen:")
    print(f"  Países comparados: {len(datos['empleados'])}")
    print(f"  Fecha: {datos['fecha_generacion']}")


if __name__ == "__main__":
    # Ejecutar todos los ejemplos comparativos
    comparacion_basica()
    comparacion_detallada()
    analisis_estructura_costos()
    comparacion_equipos()
    exportar_comparacion_completa()

    print("\n" + "=" * 70)
    print("Ejemplos comparativos completados exitosamente")
    print("=" * 70)
