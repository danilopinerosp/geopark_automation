from dash import dcc
from dash import callback_context
from dash.dependencies import Input, Output
import plotly.graph_objs as go
# Librerías para el tratamiento de datos
import numpy as np
import pandas as pd
# Importar funciones para los valores calculados del proceso
from data.calculate_values import (
    calcular_inventario_campo, 
    calcular_inventario_total,
    crudo_operacion_remitente, 
    filtrar_datos_fechas,
    total_crudo_detallado
)
from data.server import datos
from app import app

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




# Callback para actualizar la producción del último día reportado de GOV
# para Geopark
@app.callback(Output('GOV-geopark', 'figure'),
            [Input('tipo-operacion', 'value')])
def actualizar_gov_geopark(tipo_operacion):
    """
    Actualiza los datos de GOV de la producción del último día reportado
    para Geopark
    """
    # Agrupar los valores del DataFrame y hacer una suma por cada grupo
    datos_agrupados = datos.groupby(['fecha', 'empresa', 'operacion'])['GOV'].sum()
    # Seleccionar el GOV para el último día reportado
    gov_actual = np.round(datos_agrupados.unstack().unstack()[tipo_operacion]['GEOPARK'][-1], 2)
    # Seleccionar el GOV para el penúltimo día reportado
    gov_anterior = np.round(datos_agrupados.unstack().unstack()[tipo_operacion]['GEOPARK'][-2], 2)
    indicador = [go.Indicator(
                        mode='number+delta',
                        value=gov_actual,
                        delta={'reference':gov_anterior,
                                'position':'right',
                                'valueformat':',g',
                                'relative':False,
                                'font':{'size':15}},
                        number={'valueformat':',',
                                'font':{'size':20}},
                        domain={'y':[0, 1], 'x': [0, 1]}
    )]
    layout = go.Layout(title={'text':'GOV (bbls)',
                                'y':1,
                                'x':0.5,
                                'xanchor':'center',
                                'yanchor':'top'},
                        font=dict(color='orange'),
                        paper_bgcolor='#1f2c56',
                        plot_bgcolor='#1f2c56',
                        height=50)
    return {'data': indicador, 'layout':layout}

# Callback para actualizar los datos de producción de GSV de Geopark en el último día reportado
@app.callback(Output('GSV-geopark', 'figure'),
            [Input('tipo-operacion', 'value')])
def actualizar_gsv_geopark(tipo_operacion):
    """
    Actualiza la producción de GSV producida por Geopark en el último día reportado
    de producción
    """
    # Agrupar los valores del DataFrame y hacer una suma por cada grupo
    datos_agrupados = datos.groupby(['fecha', 'empresa', 'operacion'])['GSV'].sum()
    # Seleccionar el GOV para el último día reportado
    gov_actual = np.round(datos_agrupados.unstack().unstack()[tipo_operacion]['GEOPARK'][-1], 2)
    # Seleccionar el GOV para el penúltimo día reportado
    gov_anterior = np.round(datos_agrupados.unstack().unstack()[tipo_operacion]['GEOPARK'][-2], 2)
    indicador = [go.Indicator(
                        mode='number+delta',
                        value=gov_actual,
                        delta={'reference':gov_anterior,
                                'position':'right',
                                'valueformat':',g',
                                'relative':False,
                                'font':{'size':15}},
                        number={'valueformat':',',
                                'font':{'size':20}},
                        domain={'y':[0, 1], 'x': [0, 1]}
    )]
    layout = go.Layout(title={'text':'GSV (bbls)',
                                'y':1,
                                'x':0.5,
                                'xanchor':'center',
                                'yanchor':'top'},
                        font=dict(color='#dd1e35'),
                        paper_bgcolor='#1f2c56',
                        plot_bgcolor='#1f2c56',
                        height=50)
    return {'data': indicador, 'layout':layout}

# Callback para actualizar los datos de producción de NSV de Geopark en el último día reportado
@app.callback(Output('NSV-geopark', 'figure'),
            [Input('tipo-operacion', 'value')])
def actualizar_nsv_geopark(tipo_operacion):
    """
    Actualiza el NSV producido por Geopark en el último día reportado de operación
    """
    # Agrupar los valores del DataFrame y hacer una suma por cada grupo
    datos_agrupados = datos.groupby(['fecha', 'empresa', 'operacion'])['NSV'].sum()
    # Seleccionar el GOV para el último día reportado
    gov_actual = np.round(datos_agrupados.unstack().unstack()[tipo_operacion]['GEOPARK'][-1], 2)
    # Seleccionar el GOV para el penúltimo día reportado
    gov_anterior = np.round(datos_agrupados.unstack().unstack()[tipo_operacion]['GEOPARK'][-2], 2)
    indicador = [go.Indicator(
                        mode='number+delta',
                        value=gov_actual,
                        delta={'reference':gov_anterior,
                                'position':'right',
                                'valueformat':',g',
                                'relative':False,
                                'font':{'size':15}},
                        number={'valueformat':',',
                                'font':{'size':20}},
                        domain={'y':[0, 1], 'x': [0, 1]}
    )]
    layout = go.Layout(title={'text':'NSV (bbls)',
                                'y':1,
                                'x':0.5,
                                'xanchor':'center',
                                'yanchor':'top'},
                        font=dict(color='green'),
                        paper_bgcolor='#1f2c56',
                        plot_bgcolor='#1f2c56',
                        height=50)
    return {'data': indicador, 'layout':layout}

# Callback para actualizar la gráfica de participación de la empresa
@app.callback(Output('participacion-empresa', component_property='figure'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('tipo-operacion', 'value')]
)
def actualizar_participacion(start_date, end_date, value):
    """
    Actualizar el pie que contiene la participación de la empresa por tipo de operación
    en la producción de NSV
    """
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    # datos_filtrados = datos_filtrados[datos_filtrados['operacion'] == value]
    colores = ['red', 'grey']
    # Calcular total de producción diaria para NSV para determinado tipo de operación por empresa
    datos_filtrados = crudo_operacion_remitente(datos_filtrados, 'NSV', value)
    trace =[go.Pie(labels=datos_filtrados.columns.values,
                    values=[np.sum(datos_filtrados[empresa]) for empresa in datos_filtrados.columns],
                    hoverinfo='percent',
                    textinfo='label+value',
                    textfont=dict(size=13),
                    hole=.5,
                    rotation=45,
                    textposition='outside',
                    marker=dict(colors=colores))]
    layout = go.Layout(
        plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='closest',
            title={
                'text': 'Participación NSV',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                       'color': 'white',
                       'size': 25},
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="sans-serif",
                size=12,
                color='white'),
            margin=dict(t=60, b=30, l=30, r=30)
            )
    return {'data':trace, 'layout':layout}

# Callback para actualizar la gráfida de los resultados históricos de la operación para cada empresa
@app.callback(Output('NSV-historico', component_property='figure'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('tipo-operacion', 'value')]
)
def actualizar_historico(start_date, end_date, value):
    """
    Actualiza la gráfica de los resultados históricos de la operación para cada empresa
    y para el periodo de tiempo indicado
    """
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    colores = ['red', 'grey']
    datos_filtrados = crudo_operacion_remitente(datos_filtrados, 'NSV', value)
    traces = []
    for i, empresa, in enumerate(datos_filtrados.columns.values):
        traces.append(go.Scatter(x=datos_filtrados.index,
                                y=datos_filtrados[empresa],
                                name=empresa,
                                line={'width':4, 'color':colores[i]},
                                mode='lines+markers'))
    layout = go.Layout(plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='closest',
            title={
                'text': "Producción NSV histórica (bbls)",
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={'color': 'white', 'size': 25},
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="sans-serif",
                size=12,
                color='white'),
            margin=dict(t=60, b=30, l=30, r=30)
            )
    return {'data': traces, 'layout': layout}

# Callback para actualizar la gráfica de barras sobre la producción por campo
# para determinado tipo de crudo
@app.callback(Output('resultados-empresa', component_property='figure'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('tipo-operacion', 'value'),
            Input('condiciones-operacion', 'value')]
)
def actualizar_resultado_empresa(start_date, end_date, tipo_operacion, tipo_crudo):
    """
    Actualiza la gráfica de barras sobre la producción por campo para determinado tipoo de crudo
    """
    # Filtrar los datos para el período indicado, el tipo de operación de interés y el tipo de crudo
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    datos_filtrados = total_crudo_detallado(datos_filtrados, tipo_operacion)[tipo_crudo]
    traces = []
    colores = ['red', 'grey']
    for i, empresa in enumerate(datos_filtrados.index):
        traces.append(go.Bar(name=empresa,
                    x=datos_filtrados.columns.values,
                    y=datos_filtrados.loc[empresa, :],
                    marker={'color': colores[i]},
                    text=datos_filtrados.loc[empresa, :].round(2),
                    textposition='auto'))

    layout = go.Layout(title={'text':f'Producción {tipo_crudo} por Campo (bbls)',
                                'y': 0.93,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                        titlefont={'color': 'white', 'size': 20},
                        font=dict(color='white'),
                        paper_bgcolor='#1f2c56',
                        plot_bgcolor='#1f2c56',
                        barmode='stack'
                        )
    return {'data':traces, 'layout':layout}

# Callback para actualizar la gráfica de barras sobre el inventario por campo
# para determinado tipo de crudo
@app.callback(Output('inventario-empresa', component_property='figure'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('empresa', 'value'),
            Input('condiciones-operacion', 'value')])
def actualizar_inventario(start_date, end_date, empresa, tipo_crudo):
    """
    Actualiza la gráfica del inventario por empresa y por tipo de crudo
    """
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    inventario_campo = calcular_inventario_campo(datos_filtrados, empresa, tipo_crudo)
    trace = [go.Bar(name=empresa,
                    x=inventario_campo.index,
                    y=inventario_campo.values,
                    text=inventario_campo.values.round(2),
                    textposition='auto')]

    layout = go.Layout(title={'text':f'Inventario {tipo_crudo}: {empresa} por Campo (bbls)',
                                'y':0.93,
                                'x':0.5,
                                'xanchor':'center',
                                'yanchor':'top'},
                        titlefont={'color': 'white', 'size': 20},
                        font=dict(color='white'),
                        paper_bgcolor='#1f2c56',
                        plot_bgcolor='#1f2c56',
                        )
    return {'data':trace, 'layout':layout}

# Callback para mostrar el inventario total para determinado periodo, empresa y tipo de crudo
@app.callback(Output('inventario-total', component_property='children'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('empresa', 'value'),
            Input('condiciones-operacion', 'value')])
def actualizar_inventario_total(start_date, end_date, empresa, tipo_crudo):
    """
    Actualiza el inventario total por empresa y tipo de crudo para el
    periodo de tiempo indicado
    """
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    inventario_campo = calcular_inventario_campo(datos_filtrados, empresa, tipo_crudo)
    inventario_total = calcular_inventario_total(inventario_campo)
    return f'Inventario Total: {round(inventario_total, 2)}'
