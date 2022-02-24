# Librería para trabajar con fechas
from datetime import datetime as dt
# Librerías necesarias para la realización del dashboard
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
# Librerías para el tratamiento de datos
import pandas as pd
import numpy as np
# Importar constantes del proceso
from obtener_datos import CONDICIONES, EMPRESAS
# Importar funciones para los valores calculados del proceso
from procesar_datos import calcular_inventario_campo, calcular_inventario_total
from procesar_datos import crudo_operacion_remitente, filtrar_datos_fechas
from procesar_datos import total_crudo_detallado

# Cargos los datos del balance
datos = pd.read_csv('balance.csv')
# Convertir las fechas al tipo de dato datatime
datos['fecha'] = pd.to_datetime(datos['fecha'], format='%d-%m-%Y')

# Declarar el objeto app para el dashboard
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

# Generar del dashboard
app.layout = html.Div([
    # Contenedor para el encabezado
    html.Div([
        # Contenedor para el logo de Geopark
        html.Div([
            html.Img(src=app.get_asset_url('logo_geopark.png'),
                     id='logo_geopark',
                     style={
                         "height": "100px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     )
        ],
            className="one-third column",
        ),
        # Contenedor para el título del dashboard
        html.Div([
            html.Div([
                html.H2("Geopark", style={"margin-bottom": "0px", 'color': 'white'}),
                html.H5("Resultados de la operación",
                        style={"margin-top": "0px", 'color': 'white'}),
            ])
        ], className="one-half column", id="title"),
        # Contenedor para la fecha de la última actualización (último reporte contenido
        # en el análisis)
        html.Div([
            html.H6(f"Última actualización: {datos['fecha'].iloc[-1].strftime('%d/%m/%Y')}",
                    style={'color': 'orange'}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),
    # Contenedor donde se ubicaran los 6 acumulados por tipo de crudo para las dos empresas
    html.Div([
        # Contenedor GOV cumulado por tipo de operación en el periodo indicado de Geopark
        html.Div([
            html.H6(children='Geopark GOV (bbls)',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            html.P(style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 25},
                       id='GOV-acumulado-geopark'
                   )], className="card_container two columns",
        ),
        # Contenedor GSV cumulado por tipo de operación en el periodo indicado de Geopark
        html.Div([
            html.H6(children='Geopark GSV (bbls)',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 25},
                    id='GSV-acumulado-geopark'
                   )], className="card_container two columns",
        ),
        # Contenedor NSV cumulado por tipo de operación en el periodo indicado de Geopark
        html.Div([
            html.H6(children='Geopark NSV (bbls)',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 25},
                    id='NSV-acumulado-geopark'
                   )], className="card_container two columns",
        ),
        # Contenedor GOV cumulado por tipo de operación en el periodo indicado de Parex
        html.Div([
            html.H6(children='Parex GOV (bbls)',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 25},
                    id='GOV-acumulado-parex'
                   )], className="card_container two columns"),
        # Contenedor GSV cumulado por tipo de operación en el periodo indicado de Parex
        html.Div([
            html.H6(children='Parex GSV (bbls)',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 25},
                    id='GSV-acumulado-parex'
                   )], className="card_container two columns"),
        # Contenedor NSV cumulado por tipo de operación en el periodo indicado de Parex
        html.Div([
            html.H6(children='Parex NSV (bbls)',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 25},
                    id='NSV-acumulado-parex'
                   )], className="card_container two columns")

    ], className="row flex-display"),
    # Contenedor para la participación de Geopark, le operación del día y la producción
    # histórica
    html.Div([
        # Contenedor para mostrar los resultado de la operación de la fecha más reciente
        # de actualización para Geopark y generar los filtros por fecha y tipo de operación
        html.Div([
            html.P('Periodo de Análisis',
                    className='fix_label',
                    style={'color':'white', 'text-align':'center'}),
            # Permite seleccionar las fechas en las que se quiere realizar el análisis
            dcc.DatePickerRange(
                id='periodo-analisis',
                # Las fechas mínimas y máximas permitidas dependerán de las fechas
                # de los datos del balance
                min_date_allowed=datos['fecha'].min().to_pydatetime(),
                max_date_allowed=datos['fecha'].max().to_pydatetime(),
                initial_visible_month=dt(datos['fecha'].dt.year.max(),
                                        datos['fecha'].max().to_pydatetime().month, 1),
                # Por defecto toma como periodo de análisis los datos recolectados del último mes.
                start_date=(datos[datos['fecha'].dt.month == dt.today().month]['fecha'].min()).to_pydatetime(),
                end_date=datos['fecha'].max().to_pydatetime(),
                display_format='DD/MM/Y'
            ),
            # Filtrar datos según el tipo de operación (entrega, recibo, despacho)
            html.P('Tipo de Operación a analizar',
                    className='fix_label',
                    style={'color':'white', 'text-align':'center'}),
            dcc.Dropdown(options=datos['operacion'].unique(),
                        value='RECIBO POR REMITENTE TIGANA',
                        clearable=False,
                        id='tipo-operacion',
                        multi=False),
            html.P(f"Operación Geopark: {datos['fecha'].iloc[-1].strftime('%d/%m/%Y')}",
                className='fix_label', style={'color':'white', 'text-align':'center'}),
            dcc.Graph(id='GOV-geopark', config={'displayModeBar':False}, className='dcc_compon',
                    style={'margin-top':'20px'}),
            dcc.Graph(id='GSV-geopark', config={'displayModeBar':False}, className='dcc_compon',
                    style={'margin-top':'20px'}),
            dcc.Graph(id='NSV-geopark', config={'displayModeBar':False}, className='dcc_compon',
                    style={'margin-top':'20px'})
        ], className='create_container four columns'),
        # Contenedor para graficar la participación en la producción por empresa
        # (según la operación elegida)
        html.Div([
            dcc.Graph(id='participacion-empresa',
                    config={'displayModeBar':'hover'})
        ], className='create_container four columns'),
        # Contenedor para graficar la producción histórica por tipo de empresa y condición
        # de operación
        html.Div([
            dcc.Graph(id='NSV-historico')
        ], className='create_container six columns'),
    ], className='row flex-display'),
    # Contenedor para la gráfica de la producción por campo y empresa y par la gráfica de inventario
    html.Div([
        html.Div([
            dcc.Graph(id='resultados-empresa'),
        ], className='create_container six columns'),
        html.Div([
            dcc.Graph(id='inventario-empresa'),
            html.H6(id='inventario-total',
                    className='create_container_inv_total',
                    style={'color':'white','text-align':'center'}),
            html.Div([
                dcc.RadioItems(options=EMPRESAS,
                    value='GEOPARK',
                    id='empresa',
                    inline=True)
            ], style={'color':'white', 'text-align':'center'})
        ], className='create_container six columns'),
        # Filtrar datos según el tipo de operación (entrega, recibo, despacho)
    ], className='row flex-display'),
    # Contenedor para generar el filtro sobre el tipo de crudo
    html.Div([
        dcc.RadioItems(options=CONDICIONES,
            value='NSV',
            id='condiciones-operacion',
            inline=True)
        ], style={'color':'white', 'text-align':'center'})
], id='mainContainer', style={'display':'flex', 'flex-direction':'column'})

# Callback para actualizar el GOV acumulado para geopark
@app.callback(Output('GOV-acumulado-geopark', 'children'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('tipo-operacion', 'value')])
def actualizar_gov_acumulado_geopark(start_date, end_date, tipo_operacion):
    """
    Actualiza el GOV acumulado para Geopark en el periodo indicado
    """
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    datos_filtrados = datos_filtrados[['empresa', 'operacion', 'GOV']]
    filtro = (datos_filtrados['operacion'] == tipo_operacion) & (datos_filtrados['empresa'] == 'GEOPARK')
    gov_acumulado = datos_filtrados[filtro]['GOV'].sum()
    return f"{gov_acumulado:,.2f}"

# Callback para actualizar el GSV acumulado para geopark
@app.callback(Output('GSV-acumulado-geopark', 'children'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('tipo-operacion', 'value')])
def actualizar_gsv_acumulado_geopark(start_date, end_date, tipo_operacion):
    """
    Actualiza el total de GSV producido por Geopark en periodo de tiempo indicado
    """
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    datos_filtrados = datos_filtrados[['empresa', 'operacion', 'GSV']]
    filtro = (datos_filtrados['operacion'] == tipo_operacion) & (datos_filtrados['empresa'] == 'GEOPARK')
    gsv_acumulado = datos_filtrados[filtro]['GSV'].sum()
    return f"{gsv_acumulado:,.2f}"

# Callback para actualizar el NSV acumulado para Geopark
@app.callback(Output('NSV-acumulado-geopark', 'children'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('tipo-operacion', 'value')])
def actualizar_nsv_acumulado_geopark(start_date, end_date, tipo_operacion):
    """
    Actualiza en acumulado de NSV producido por Geopark en el periodo de tiempo indicado
    """
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    datos_filtrados = datos_filtrados[['empresa', 'operacion', 'NSV']]
    filtro = (datos_filtrados['operacion'] == tipo_operacion) & (datos_filtrados['empresa'] == 'GEOPARK')
    gov_acumulado = datos_filtrados[filtro]['NSV'].sum()
    return f"{gov_acumulado:,.2f}"

# Callback para actualizar el NSV acumulado para Parex
@app.callback(Output('GOV-acumulado-parex', 'children'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('tipo-operacion', 'value')])
def actualizar_gov_acumulado_parex(start_date, end_date, tipo_operacion):
    """
    Actualiza el GOV acumulado en el periodo indicado para Parex
    """
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    datos_filtrados = datos_filtrados[['empresa', 'operacion', 'GOV']]
    filtro = (datos_filtrados['operacion'] == tipo_operacion) & (datos_filtrados['empresa'] == 'PAREX')
    gov_acumulado = datos_filtrados[filtro]['GOV'].sum()
    return f"{gov_acumulado:,.2f}"

# Callback para actualizar el GSV acumulado para Parex
@app.callback(Output('GSV-acumulado-parex', 'children'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('tipo-operacion', 'value')])
def actualizar_gsv_acumulado_parex(start_date, end_date, tipo_operacion):
    """
    Actualiza el GSV acumulado producido por Parex en el periodo de tiempo indicado
    """
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    datos_filtrados = datos_filtrados[['empresa', 'operacion', 'GSV']]
    filtro = (datos_filtrados['operacion'] == tipo_operacion) & (datos_filtrados['empresa'] == 'PAREX')
    gsv_acumulado = datos_filtrados[filtro]['GSV'].sum()
    return f"{gsv_acumulado:,.2f}"

# Callback para actualizar el NSV acumulado para Parex
@app.callback(Output('NSV-acumulado-parex', 'children'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('tipo-operacion', 'value')])
def actualizar_nsv_acumulado_parex(start_date, end_date, tipo_operacion):
    """
    Actualiza el total de NSV acumulado para Parex en el periodo de tiempo indicado
    """
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    datos_filtrados = datos_filtrados[['empresa', 'operacion', 'NSV']]
    filtro = (datos_filtrados['operacion'] == tipo_operacion) & (datos_filtrados['empresa'] == 'PAREX')
    nsv_acumulado = datos_filtrados[filtro]['NSV'].sum()
    return f"{nsv_acumulado:,.2f}"

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
    datos_filtrados = crudo_operacion_remitente(datos, 'NSV', value)
    traces = []
    for i, empresa, in enumerate(datos_filtrados.columns.values):
        traces.append(go.Scatter(x=datos_filtrados.index,
                                y=datos_filtrados[empresa],
                                name=empresa,
                                line={'width':4, 'color':colores[i]}))
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
    datos_filtrados = total_crudo_detallado(datos, tipo_operacion)[tipo_crudo]
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

if __name__ == '__main__':
    app.run_server(debug=True)
