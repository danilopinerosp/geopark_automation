from dash.dependencies import Input, Output
# Importar funciones para los valores calculados del proceso
from calculate_values import filtrar_datos_fechas
from server import app, datos

def calcular_acumulado(datos, start_date, end_date, tipo_operacion, tipo_crudo, empresa):
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    datos_filtrados = datos_filtrados[['empresa', 'operacion', tipo_crudo]]
    filtro = (datos_filtrados['operacion'] == tipo_operacion) & (datos_filtrados['empresa'] == empresa)
    gov_acumulado = datos_filtrados[filtro][tipo_crudo].sum()
    return f"{gov_acumulado:,.2f}"


inputs = [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('tipo-operacion', 'value')]

# Callback para actualizar el GOV acumulado para geopark
@app.callback(Output('GOV-acumulado-geopark', 'children'), inputs)
def actualizar_gov_acumulado_geopark(start_date, end_date, tipo_operacion):
    """
    Actualiza el GOV acumulado para Geopark en el periodo indicado
    """
    return calcular_acumulado(datos, start_date, end_date, tipo_operacion, 'GOV', 'GEOPARK')

# Callback para actualizar el GSV acumulado para geopark
@app.callback(Output('GSV-acumulado-geopark', 'children'), inputs)
def actualizar_gsv_acumulado_geopark(start_date, end_date, tipo_operacion):
    """
    Actualiza el total de GSV producido por Geopark en periodo de tiempo indicado
    """
    return calcular_acumulado(datos, start_date, end_date, tipo_operacion, 'GSV', 'GEOPARK')

# Callback para actualizar el NSV acumulado para Geopark
@app.callback(Output('NSV-acumulado-geopark', 'children'), inputs)
def actualizar_nsv_acumulado_geopark(start_date, end_date, tipo_operacion):
    """
    Actualiza en acumulado de NSV producido por Geopark en el periodo de tiempo indicado
    """
    return calcular_acumulado(datos, start_date, end_date, tipo_operacion, 'NSV', 'GEOPARK')

# Callback para actualizar el NSV acumulado para Parex
@app.callback(Output('GOV-acumulado-parex', 'children'), inputs)
def actualizar_gov_acumulado_parex(start_date, end_date, tipo_operacion):
    """
    Actualiza el GOV acumulado en el periodo indicado para Parex
    """
    return calcular_acumulado(datos, start_date, end_date, tipo_operacion, 'GOV', 'PAREX')

# Callback para actualizar el GSV acumulado para Parex
@app.callback(Output('GSV-acumulado-parex', 'children'), inputs)
def actualizar_gsv_acumulado_parex(start_date, end_date, tipo_operacion):
    """
    Actualiza el GSV acumulado producido por Parex en el periodo de tiempo indicado
    """
    return calcular_acumulado(datos, start_date, end_date, tipo_operacion, 'GSV', 'PAREX')

# Callback para actualizar el NSV acumulado para Parex
@app.callback(Output('NSV-acumulado-parex', 'children'), inputs)
def actualizar_nsv_acumulado_parex(start_date, end_date, tipo_operacion):
    """
    Actualiza el total de NSV acumulado para Parex en el periodo de tiempo indicado
    """
    return calcular_acumulado(datos, start_date, end_date, tipo_operacion, 'NSV', 'PAREX')
