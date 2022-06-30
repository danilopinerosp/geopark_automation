import numpy as np

from data.server import datos
from data.calculate_values import filtrar_datos_fechas

def calcular_acumulado(datos, start_date, end_date, tipo_operacion, tipo_crudo, empresa):
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    datos_filtrados = datos_filtrados[['empresa', 'operacion', tipo_crudo]]
    filtro = (datos_filtrados['operacion'] == tipo_operacion) & (datos_filtrados['empresa'] == empresa)
    gov_acumulado = datos_filtrados[filtro][tipo_crudo].sum()
    return f"{gov_acumulado:,.2f}"

def update_indicators(data, operation_type, operation_conditions):
    # Agrupar los valores del DataFrame y hacer una suma por cada grupo
    datos_agrupados = data.groupby(['fecha', 'empresa', 'operacion'])[operation_conditions].sum()
    # Seleccionar el GOV para el último día reportado
    last = np.round(datos_agrupados.unstack().unstack()[operation_type]['GEOPARK'][-1], 2)
    # Seleccionar el GOV para el penúltimo día reportado
    previous = np.round(datos_agrupados.unstack().unstack()[operation_type]['GEOPARK'][-2], 2)
    return (last, previous)