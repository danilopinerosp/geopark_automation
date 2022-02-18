import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
# from obtener_datos import CONDICIONES
from datetime import datetime as dt
from datetime import date, timedelta
import numpy as np
from obtener_datos import CONDICIONES

from procesar_datos import crudo_operacion_remitente, filtrar_datos_fechas, total_crudo, total_crudo_detallado, total_crudo_empresa

# Cargos los datos del balance
datos = pd.read_csv('balance.csv')
# Convertir las fechas al tipo de dato datatime
datos['fecha'] = pd.to_datetime(datos['fecha'], format='%d-%m-%Y')

# Calcular los acumulados por tipo de operación de las condiciones de operación para NSV
total_entrega = total_crudo(datos, 'ENTREGA')['NSV']
total_despacho = total_crudo(datos, 'DESPACHO')['NSV']
total_recibo = total_crudo(datos, 'RECIBO')['NSV']
# Calcular el total de entregas de NSV acumuladas para Geopark
entregas_geopark = total_crudo_empresa(datos, 'ENTREGA').loc['GEOPARK', 'NSV']

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
                html.H5("Resultados de la operación", style={"margin-top": "0px", 'color': 'white'}),
            ])
        ], className="one-half column", id="title"),
        # Contenedor para la fecha de la última actualización (último reporte contenido en el análisis)
        html.Div([
            html.H6(f"Última actualización: {datos['fecha'].iloc[-1].strftime('%d/%m/%Y')}",
                    style={'color': 'orange'}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),
    # Contenedor donde se ubicaran los 4 principales datos acumulados del dashboard
    html.Div([
        # Contenedor GOV cumulado por tipo de operación en el periodo indicado de todas las empresas
        html.Div([
            html.H6(children='GOV (bbls)',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{total_entrega:,.2f}", # formatea el valor a 2 decimales
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   )], className="card_container three columns",
        ),
        # Contenedor GSV cumulado por tipo de operación en el periodo indicado de todas las empresas
        html.Div([
            html.H6(children='GSV (bbls)',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{total_despacho:,.2f}",
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 40}
                   )], className="card_container three columns",
        ),
        # Contenedor NSV cumulado por tipo de operación en el periodo indicado de todas las empresas
        html.Div([
            html.H6(children='NSV (bbls)',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{total_recibo:,.2f}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 40}
                   )], className="card_container three columns",
        ),
        # Contenedor NSV acumulado por tipo de operación en el periodo indicado para Geopark
        html.Div([
            html.H6(children='NSV Geopark (bbls)',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{entregas_geopark:,.2f}",
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 40}
                   )], className="card_container three columns")

    ], className="row flex-display"),
    # Contenedor para crear los dos filtros (periodo de análisis y tipo de operación)
    html.Div([
        # Contenedor para la selección del período de análisis
        html.Div([
            html.P('Periodo de Análisis', className='fix_label', style={'color':'white'}),
            # Permite seleccionar las fechas en las que se quiere realizar el análisis
            dcc.DatePickerRange(
                id='periodo-analisis',
                # Las fechas mínimas y máximas permitidas dependerán de las fechas de los datos del balance
                min_date_allowed=datos['fecha'].min().to_pydatetime(),
                max_date_allowed=datos['fecha'].max().to_pydatetime(),
                initial_visible_month=dt(datos['fecha'].dt.year.max(), datos['fecha'].max().to_pydatetime().month, 1),
                # Por defecto toma como periodo de análisis los datos recolectados del último mes.
                start_date=(datos[datos['fecha'].dt.month == dt.today().month]['fecha'].min()).to_pydatetime(),
                end_date=datos['fecha'].max().to_pydatetime(),
                display_format='DD/MM/Y'
            ),
        ], className='create_container four columns'),
        # Contenedor para la selección del tipo de operación a analizar
        html.Div([
            # Filtrar datos según el tipo de operación (entrega, recibo, despacho)
            html.P('Tipo de Operación a analizar', className='fix_label', style={'color':'white'}),
            dcc.Dropdown(options=datos['operacion'].unique(),
                        value='RECIBO POR REMITENTE TIGANA',
                        clearable=False,
                        id='tipo-operacion',
                        multi=False)
        ], className='create_container eight columns', id='cross-filter-options')
    ], id="filtro-analisis", className="row flex-display"),
    # Contenedor para la participación de Geopark, le operación del día y la producción histórica
    html.Div([
        # Contenedor para mostrar los resultado de la operación de la fecha más reciente de actualización
        # para Geopark
        html.Div([
            html.P(f"Operación Geopark: {datos['fecha'].iloc[-1].strftime('%d/%m/%Y')}",
                className='fix_label', style={'color':'white', 'text-align':'center'}),
            dcc.Graph(id='GOV-geopark', config={'displayModeBar':False}, className='dcc_compon',
                    style={'margin-top':'20px'}), 
            dcc.Graph(id='GSV-geopark', config={'displayModeBar':False}, className='dcc_compon',
                    style={'margin-top':'20px'}), 
            dcc.Graph(id='NSV-geopark', config={'displayModeBar':False}, className='dcc_compon',
                    style={'margin-top':'20px'})
        ], className='create_container four columns'), 
        # Contenedor para graficar la participación en la producción por empresa (según la operación elegida)
        html.Div([
            dcc.Graph(id='participacion-empresa',
                    config={'displayModeBar':'hover'})
        ], className='create_container four columns'),
        # Contenedor para graficar la producción histórica por tipo de empresa y condición de operación
        html.Div([
            dcc.Graph(id='NSV-historico')
        ], className='create_container six columns'),
    ], className='row flex-display'),
    # Contenedor para crear el filtro sobre las condiciones de operación del crudo (GOV, GSV, NSV)
    html.Div([
            # Filtrar datos según el tipo de operación (entrega, recibo, despacho)
            html.P('Tipo de Crudo', className='fix_label', style={'color':'white'}),
            dcc.Dropdown(options=CONDICIONES,
                        value='NSV',
                        clearable=False,
                        id='condiciones-operacion',
                        multi=False)
        ], className='create_container twelve columns'),
    # Contenedor para la gráfica de la producción por campo y empresa.
    html.Div([
        html.Div(
            [dcc.Graph(id='resultados-empresa')
        ], className='create_container1 twelve columns'),
    ], className='row flex-display'),
], id='mainContainer', style={'display':'flex', 'flex-direction':'column'})

@app.callback(Output('GOV-geopark', 'figure'),
            [Input('tipo-operacion', 'value')])
def actualizar_GOV_geopark(tipo_operacion):
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
def actualizar_GSV_geopark(tipo_operacion):
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
def actualizar_NSV_geopark(tipo_operacion):
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
                'text': f"Producción NSV histórica (bbls)",
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
    return {'data': traces, 'layout': layout}

# Callback para actualizar la gráfica de barras sobre la producción por campo para determinado tipo de crudo
@app.callback(Output('resultados-empresa', component_property='figure'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('tipo-operacion', 'value'),
            Input('condiciones-operacion', 'value')]
)
def actualizar_resultado_empresa(start_date, end_date, tipo_operacion, tipo_crudo):
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

    layout = go.Layout(title={'text':'Producción NSV por Campo (bbls)',
                                'y':1,
                                'x':0.5,
                                'xanchor':'center',
                                'yanchor':'top'},
                        font=dict(color='white'),
                        paper_bgcolor='#1f2c56',
                        plot_bgcolor='#1f2c56',
                        barmode='stack'
                        )
    return {'data':traces, 'layout':layout}    

if __name__ == '__main__':
    app.run_server(debug=True)
