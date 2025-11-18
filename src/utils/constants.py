"""
Constantes y configuraciones del sistema
"""

# Tasas y valores para Perú (2024)
PERU = {
    'codigo': 'PE',
    'moneda': 'PEN',
    'nombre': 'Perú',
    'tasas': {
        'essalud': 0.09,
        'afp_empleador': 0.0013,
        'sctr': 0.0063,
        'asignacion_familiar': 0.10
    },
    'valores': {
        'salario_minimo': 1025,
        'uit': 5150  # Unidad Impositiva Tributaria 2024
    }
}

# Tasas y valores para Colombia (2024)
COLOMBIA = {
    'codigo': 'CO',
    'moneda': 'COP',
    'nombre': 'Colombia',
    'tasas': {
        'salud': 0.085,
        'pension': 0.12,
        'caja_compensacion': 0.04,
        'icbf': 0.03,
        'sena': 0.02,
        'intereses_cesantias': 0.12
    },
    'tasas_arl': {
        1: 0.00522,
        2: 0.01044,
        3: 0.02436,
        4: 0.04350,
        5: 0.06960
    },
    'valores': {
        'salario_minimo': 1300000,
        'auxilio_transporte': 162000
    }
}

# Configuración general
CONFIGURACION = {
    'periodo_default': 'mensual',
    'decimales': 2,
    'formato_fecha': '%Y-%m-%d',
    'formato_hora': '%H:%M:%S'
}
