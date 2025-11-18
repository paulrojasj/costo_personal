"""
Generador de reportes y métricas de costo de personal
"""

from typing import List, Dict, Any
import json
from datetime import datetime


class ReportGenerator:
    """Generador de reportes de costos de personal"""

    def __init__(self, calculators: List[Any]):
        """
        Inicializa el generador de reportes

        Args:
            calculators: Lista de instancias de calculadoras (Peru, Colombia)
        """
        self.calculators = calculators if isinstance(calculators, list) else [calculators]

    def generar_reporte_individual(self, calculator: Any) -> str:
        """Genera un reporte individual para una calculadora"""
        costo = calculator.calcular_costo_total()
        metricas = calculator.get_metricas()

        pais = costo['pais']
        moneda = costo['moneda']

        reporte = []
        reporte.append("=" * 70)
        reporte.append(f"REPORTE DE COSTO DE PERSONAL - {pais}")
        reporte.append("=" * 70)
        reporte.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        reporte.append(f"Moneda: {moneda}")
        reporte.append("")

        # Información básica
        reporte.append("INFORMACIÓN BÁSICA:")
        reporte.append("-" * 70)
        reporte.append(f"  Salario Base:              {moneda} {costo['salario_base']:,.2f}")

        # Desglose mensual
        reporte.append("")
        reporte.append("DESGLOSE DE COSTOS MENSUALES:")
        reporte.append("-" * 70)

        desglose = costo['desglose_mensual']
        reporte.append(f"  Salario Base:              {moneda} {desglose['salario_base']:,.2f}")

        if 'auxilio_transporte' in desglose:
            reporte.append(f"  Auxilio de Transporte:     {moneda} {desglose['auxilio_transporte']:,.2f}")

        reporte.append(f"  Cargas Sociales:           {moneda} {desglose['cargas_sociales']:,.2f}")

        if 'beneficios_prorrateados' in desglose:
            reporte.append(f"  Beneficios (prorrateados): {moneda} {desglose['beneficios_prorrateados']:,.2f}")
        elif 'prestaciones_prorrateadas' in desglose:
            reporte.append(f"  Prestaciones (prorrateadas): {moneda} {desglose['prestaciones_prorrateadas']:,.2f}")

        reporte.append("  " + "-" * 68)
        reporte.append(f"  COSTO TOTAL MENSUAL:       {moneda} {desglose['total']:,.2f}")

        # Cargas sociales detalladas
        reporte.append("")
        reporte.append("DETALLE DE CARGAS SOCIALES:")
        reporte.append("-" * 70)

        cargas = costo['cargas_sociales']
        for concepto, valor in cargas.items():
            if concepto not in ['total_cargas', 'porcentaje_total', 'arl_nivel']:
                nombre = concepto.replace('_', ' ').title()
                reporte.append(f"  {nombre:30} {moneda} {valor:,.2f}")

        # Beneficios/Prestaciones detalladas
        reporte.append("")
        if pais == 'PE':
            reporte.append("DETALLE DE BENEFICIOS:")
        else:
            reporte.append("DETALLE DE PRESTACIONES SOCIALES:")
        reporte.append("-" * 70)

        beneficios = costo['beneficios']
        conceptos_anuales = {k: v for k, v in beneficios.items() if 'anual' in k}

        for concepto, valor in conceptos_anuales.items():
            nombre = concepto.replace('_anual', '').replace('_', ' ').title()
            reporte.append(f"  {nombre:30} {moneda} {valor:,.2f} (anual)")

        # Métricas clave
        reporte.append("")
        reporte.append("MÉTRICAS CLAVE:")
        reporte.append("-" * 70)
        reporte.append(f"  Costo efectivo vs salario: {metricas['costo_efectivo_vs_salario']}")
        reporte.append(f"  Incremento sobre salario:  {metricas['incremento_porcentual']}")
        reporte.append(f"  Costo adicional mensual:   {moneda} {metricas['costo_adicional_mensual']:,.2f}")
        reporte.append(f"  Proyección anual:          {moneda} {metricas['proyeccion_anual']:,.2f}")

        reporte.append("=" * 70)
        reporte.append("")

        return "\n".join(reporte)

    def generar_reporte_comparativo(self) -> str:
        """Genera un reporte comparativo entre países"""
        if len(self.calculators) < 2:
            return "Se necesitan al menos 2 calculadoras para generar un reporte comparativo"

        reporte = []
        reporte.append("=" * 70)
        reporte.append("REPORTE COMPARATIVO DE COSTOS DE PERSONAL")
        reporte.append("=" * 70)
        reporte.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        reporte.append("")

        datos_comparacion = []

        for calc in self.calculators:
            costo = calc.calcular_costo_total()
            metricas = calc.get_metricas()

            datos_comparacion.append({
                'pais': costo['pais'],
                'moneda': costo['moneda'],
                'salario_base': costo['salario_base'],
                'costo_mensual': costo['costo_mensual'],
                'costo_anual': costo['costo_anual'],
                'ratio': costo['ratio_costo_salario'],
                'incremento': metricas['incremento_porcentual']
            })

        # Tabla comparativa
        reporte.append("COMPARACIÓN DE COSTOS:")
        reporte.append("-" * 70)
        reporte.append(f"{'País':^10} | {'Salario Base':>18} | {'Costo Mensual':>18} | {'Ratio':>8}")
        reporte.append("-" * 70)

        for dato in datos_comparacion:
            reporte.append(
                f"{dato['pais']:^10} | "
                f"{dato['moneda']} {dato['salario_base']:>12,.2f} | "
                f"{dato['moneda']} {dato['costo_mensual']:>12,.2f} | "
                f"{dato['ratio']:>8.2f}x"
            )

        reporte.append("")
        reporte.append("INCREMENTO SOBRE SALARIO BASE:")
        reporte.append("-" * 70)

        for dato in datos_comparacion:
            reporte.append(f"  {dato['pais']}: {dato['incremento']}")

        reporte.append("=" * 70)
        reporte.append("")

        return "\n".join(reporte)

    def exportar_json(self, archivo: str = None) -> Dict[str, Any]:
        """
        Exporta los datos a formato JSON

        Args:
            archivo: Ruta del archivo (opcional)

        Returns:
            Diccionario con los datos
        """
        datos = {
            'fecha_generacion': datetime.now().isoformat(),
            'empleados': []
        }

        for calc in self.calculators:
            costo = calc.calcular_costo_total()
            metricas = calc.get_metricas()

            datos['empleados'].append({
                'pais': costo['pais'],
                'costos': costo,
                'metricas': metricas
            })

        if archivo:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)

        return datos

    def generar_resumen_ejecutivo(self) -> str:
        """Genera un resumen ejecutivo consolidado"""
        reporte = []
        reporte.append("=" * 70)
        reporte.append("RESUMEN EJECUTIVO - COSTOS DE PERSONAL")
        reporte.append("=" * 70)
        reporte.append("")

        total_empleados = len(self.calculators)
        reporte.append(f"Total de empleados analizados: {total_empleados}")
        reporte.append("")

        costo_total_mensual = 0
        costo_total_anual = 0

        for calc in self.calculators:
            costo = calc.calcular_costo_total()
            costo_total_mensual += costo['costo_mensual']
            costo_total_anual += costo['costo_anual']

        reporte.append("CONSOLIDADO:")
        reporte.append("-" * 70)
        reporte.append(f"  Costo total mensual:  $ {costo_total_mensual:,.2f}")
        reporte.append(f"  Costo total anual:    $ {costo_total_anual:,.2f}")
        reporte.append("")

        # Desglose por país
        costos_por_pais = {}
        for calc in self.calculators:
            costo = calc.calcular_costo_total()
            pais = costo['pais']

            if pais not in costos_por_pais:
                costos_por_pais[pais] = {
                    'cantidad': 0,
                    'costo_mensual': 0,
                    'costo_anual': 0
                }

            costos_por_pais[pais]['cantidad'] += 1
            costos_por_pais[pais]['costo_mensual'] += costo['costo_mensual']
            costos_por_pais[pais]['costo_anual'] += costo['costo_anual']

        reporte.append("DESGLOSE POR PAÍS:")
        reporte.append("-" * 70)

        for pais, datos in costos_por_pais.items():
            reporte.append(f"  {pais}:")
            reporte.append(f"    Empleados:        {datos['cantidad']}")
            reporte.append(f"    Costo mensual:    $ {datos['costo_mensual']:,.2f}")
            reporte.append(f"    Costo anual:      $ {datos['costo_anual']:,.2f}")
            reporte.append("")

        reporte.append("=" * 70)
        reporte.append("")

        return "\n".join(reporte)
