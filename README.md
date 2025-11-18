# Sistema de Cálculo de Costo de Personal

Sistema completo de cálculo de costos de personal para **Perú (PE)** y **Colombia (CO)**, incluyendo reportería y métricas clave para la gestión de recursos humanos.

## Características

- **Cálculo preciso de costos laborales** según legislación vigente de cada país (2024)
- **Cargas sociales** completas (EsSalud, AFP, Salud, Pensión, ARL, etc.)
- **Beneficios y prestaciones** (gratificaciones, CTS, prima de servicios, cesantías, etc.)
- **Reportería detallada** con desgloses y métricas clave
- **Comparaciones** entre países y equipos
- **Exportación a JSON** para integración con otros sistemas
- **Arquitectura modular** y fácilmente extensible

## Estructura del Proyecto

```
costo_personal/
├── src/
│   ├── calculators/
│   │   ├── base.py           # Clase base abstracta
│   │   ├── peru.py           # Calculadora para Perú
│   │   └── colombia.py       # Calculadora para Colombia
│   ├── reports/
│   │   └── generator.py      # Generador de reportes
│   └── utils/
│       └── constants.py      # Constantes y configuraciones
├── examples/
│   ├── ejemplo_peru.py       # Ejemplos de uso para Perú
│   ├── ejemplo_colombia.py   # Ejemplos de uso para Colombia
│   └── ejemplo_comparativo.py # Comparaciones PE vs CO
├── requirements.txt
└── README.md
```

## Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd costo_personal

# Instalar dependencias (opcional, solo para desarrollo)
pip install -r requirements.txt
```

## Uso Rápido

### Perú

```python
from src.calculators.peru import PeruPayrollCalculator
from src.reports.generator import ReportGenerator

# Crear calculadora para empleado en Perú
calc = PeruPayrollCalculator(
    salario_base=4000,        # S/ 4,000
    periodo='mensual',
    tiene_hijos=True,         # Recibe asignación familiar
    incluye_sctr=False        # Sin SCTR
)

# Obtener costos
costo = calc.calcular_costo_total()
print(f"Costo mensual total: S/ {costo['costo_mensual']:,.2f}")
print(f"Ratio costo/salario: {costo['ratio_costo_salario']}x")

# Generar reporte
generador = ReportGenerator(calc)
print(generador.generar_reporte_individual(calc))
```

### Colombia

```python
from src.calculators.colombia import ColombiaPayrollCalculator
from src.reports.generator import ReportGenerator

# Crear calculadora para empleado en Colombia
calc = ColombiaPayrollCalculator(
    salario_base=3500000,     # $3,500,000 COP
    periodo='mensual',
    nivel_arl=1               # Nivel de riesgo I (mínimo)
)

# Obtener costos
costo = calc.calcular_costo_total()
print(f"Costo mensual total: ${costo['costo_mensual']:,.0f}")
print(f"Ratio costo/salario: {costo['ratio_costo_salario']}x")

# Generar reporte
generador = ReportGenerator(calc)
print(generador.generar_reporte_individual(calc))
```

## Conceptos Incluidos por País

### Perú (PE)

#### Cargas Sociales Empleador:
- **EsSalud**: 9% del salario bruto
- **AFP Empleador**: ~0.13% (seguro)
- **SCTR**: ~0.63% (si aplica, para trabajos de riesgo)

#### Beneficios:
- **Asignación Familiar**: 10% del salario mínimo (si tiene hijos)
- **Gratificaciones**: 2 al año (Julio y Diciembre)
- **CTS**: Compensación por Tiempo de Servicios
- **Vacaciones**: 30 días al año

**Valores de Referencia 2024:**
- Salario mínimo: S/ 1,025
- UIT: S/ 5,150

### Colombia (CO)

#### Cargas Sociales Empleador:
- **Salud**: 8.5% del salario
- **Pensión**: 12% del salario
- **ARL**: 0.522% - 6.96% según nivel de riesgo
- **Caja de Compensación**: 4%
- **ICBF**: 3%
- **SENA**: 2%

#### Prestaciones Sociales:
- **Auxilio de Transporte**: $162,000 (si salario ≤ 2 SMMLV)
- **Prima de Servicios**: 1 salario al año
- **Cesantías**: 1 salario al año
- **Intereses sobre Cesantías**: 12% anual
- **Vacaciones**: 15 días hábiles al año

**Valores de Referencia 2024:**
- Salario mínimo: $1,300,000
- Auxilio de transporte: $162,000

## Ejemplos de Uso

### Ejecutar Ejemplos

```bash
# Ejemplos para Perú
cd examples
python ejemplo_peru.py

# Ejemplos para Colombia
python ejemplo_colombia.py

# Comparaciones entre países
python ejemplo_comparativo.py
```

### Análisis de Múltiples Empleados

```python
from src.calculators.peru import PeruPayrollCalculator
from src.calculators.colombia import ColombiaPayrollCalculator
from src.reports.generator import ReportGenerator

# Crear equipo mixto
equipo = [
    PeruPayrollCalculator(salario_base=4000, tiene_hijos=True),
    PeruPayrollCalculator(salario_base=6000, tiene_hijos=False),
    ColombiaPayrollCalculator(salario_base=5000000, nivel_arl=1),
    ColombiaPayrollCalculator(salario_base=7000000, nivel_arl=2)
]

# Generar resumen ejecutivo
generador = ReportGenerator(equipo)
print(generador.generar_resumen_ejecutivo())
```

### Exportar a JSON

```python
# Exportar datos para integración
generador = ReportGenerator(calculators)
datos = generador.exportar_json('reporte_costos.json')

# Los datos incluyen:
# - fecha_generacion
# - empleados (array)
#   - pais
#   - costos (desglose completo)
#   - metricas
```

## Reportes Disponibles

### 1. Reporte Individual
Análisis detallado de un empleado:
- Salario base
- Desglose de cargas sociales
- Desglose de beneficios/prestaciones
- Métricas clave (ratio costo/salario, incremento %, proyección anual)

### 2. Reporte Comparativo
Comparación entre múltiples empleados o países:
- Tabla comparativa de costos
- Ratios costo/salario
- Incrementos porcentuales

### 3. Resumen Ejecutivo
Vista consolidada de equipos completos:
- Totales mensuales y anuales
- Desglose por país
- Cantidad de empleados

## Métricas Clave

Para cada empleado se calculan:

- **Costo Total Mensual**: Suma de salario + cargas + beneficios (prorrateados)
- **Costo Total Anual**: Proyección anual del costo
- **Ratio Costo/Salario**: Factor multiplicador del costo real vs salario base
- **Incremento Porcentual**: Porcentaje de incremento sobre el salario base
- **Costo Adicional**: Diferencia entre costo total y salario base

## Casos de Uso

### 1. Planificación de Presupuesto
```python
# Calcular costo real de nuevas contrataciones
calc = PeruPayrollCalculator(salario_base=5000)
costo = calc.calcular_costo_total()
print(f"Presupuesto anual necesario: S/ {costo['costo_anual']:,.2f}")
```

### 2. Comparación de Costos entre Países
```python
# Decidir dónde contratar basado en costos
pe = PeruPayrollCalculator(salario_base=4000)
co = ColombiaPayrollCalculator(salario_base=5000000)

gen = ReportGenerator([pe, co])
print(gen.generar_reporte_comparativo())
```

### 3. Análisis de Impacto de Beneficios
```python
# Con asignación familiar
con_hijos = PeruPayrollCalculator(salario_base=4000, tiene_hijos=True)

# Sin asignación familiar
sin_hijos = PeruPayrollCalculator(salario_base=4000, tiene_hijos=False)

# Comparar costos
```

### 4. Optimización de Estructura de Riesgos (Colombia)
```python
# Comparar costos según nivel de riesgo ARL
for nivel in range(1, 6):
    calc = ColombiaPayrollCalculator(salario_base=3000000, nivel_arl=nivel)
    metricas = calc.get_metricas()
    print(f"Nivel {nivel}: {metricas['costo_adicional_mensual']}")
```

## Extensibilidad

El sistema está diseñado para ser fácilmente extensible:

### Agregar un Nuevo País

1. Crear nueva clase en `src/calculators/nuevo_pais.py`
2. Heredar de `PayrollCalculator`
3. Implementar métodos abstractos:
   - `calcular_cargas_sociales()`
   - `calcular_beneficios()`
   - `calcular_costo_total()`

```python
from .base import PayrollCalculator

class NuevoPaisPayrollCalculator(PayrollCalculator):
    def calcular_cargas_sociales(self):
        # Implementar lógica específica
        pass

    def calcular_beneficios(self):
        # Implementar lógica específica
        pass

    def calcular_costo_total(self):
        # Implementar lógica específica
        pass
```

## Actualizaciones de Legislación

Los valores y tasas están basados en la legislación vigente de 2024. Para actualizar:

1. Modificar constantes en `src/calculators/peru.py` o `colombia.py`
2. Actualizar `src/utils/constants.py`
3. Verificar cálculos con los ejemplos

## Consideraciones Importantes

- **Valores aproximados**: Los cálculos asumen empleados con año completo trabajado
- **Variaciones**: Pueden existir variaciones según industria, convenios colectivos, etc.
- **Asesoría profesional**: Este sistema es una herramienta de apoyo, siempre consulte con profesionales de RRHH y contabilidad
- **Actualizaciones**: Verifique que las tasas y valores estén actualizados según legislación vigente

## Soporte

Para preguntas o sugerencias sobre el sistema de cálculo de costos de personal, contacte al equipo de desarrollo.

## Licencia

Este proyecto está bajo licencia MIT.

---

**Versión**: 1.0.0
**Última actualización**: Noviembre 2024
**Países soportados**: Perú (PE), Colombia (CO)
