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

from procesar_datos import filtrar_datos_fechas, nsv_despacho_remitente, nsv_recibo_remitente, total_crudo, total_crudo_detallado, total_crudo_empresa

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
    html.Div([
        # Contenedor para el logo de Geopark
        html.Div([
            html.Img(src=app.get_asset_url('logo_geopark.png'),
                     id='logo_geopark',
                     style={
                         "height": "60px",
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
                html.H3("Geopark", style={"margin-bottom": "0px", 'color': 'white'}),
                html.H5("Dashboard: Resultado de la operación", style={"margin-top": "0px", 'color': 'white'}),
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
        # Contenedor para las entregas acumuladas de NSV para todas las empresas
        html.Div([
            html.H6(children='Entregas (bbls)',
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
        # Despachos acumulados de NSV para todas las empresas
        html.Div([
            html.H6(children='Despachos (bbls)',
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
        # Recibos acumulados de NSV para todas las empresas
        html.Div([
            html.H6(children='Recibos (bbls)',
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
        # Enregas de NSV acumuladas para Geopark
        html.Div([
            html.H6(children='Entregas Geopark (bbls)',
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
    html.Div([
        # Contenedor para mostrar los resultado de la operación de la fecha más reciente de actualización
        # para Geopark
        html.Div([
            html.P(f"Resultados Operación: {datos['fecha'].iloc[-1].strftime('%d/%m/%Y')}",
                className='fix_label', style={'color':'white', 'text-align':'center'})
        ], className='create_container three columns'), 
        # Contenedor para graficar la participación en la producción por empresa (según la operación elegida)
        html.Div([
            dcc.Graph(id='participacion-empresa',
                    config={'displayModeBar':'hover'})
        ], className='create_container four columns'),
        # Contenedor para graficar la producción histórica por tipo de empresa y condición de operación
        html.Div([
            dcc.Graph(id='line_chart')
        ], className='create_container seven columns'),
    ], className='row flex-display'),
    # Contenedor para la gráfica de la producción por campo y empresa.
    html.Div([
        html.Div(
            [dcc.Graph(id='bar_chart1')
        ], className='create_container1 six columns'),
        html.Div(
            [dcc.Graph(id='bar_chart2')
        ], className='create_container1 six columns')
    ], className='row flex-display')
], id='mainContainer', style={'display':'flex', 'flex-direction':'column'})

# Callback para actualizar la gráfica de participación de la empresa
@app.callback(Output('participacion-empresa', component_property='figure'),
            [Input('periodo-analisis', 'start_date'),
            Input('periodo-analisis', 'end_date'),
            Input('tipo-operacion', 'value')]
)
def actualizar_participacion(start_date, end_date, value):
    datos_filtrados = filtrar_datos_fechas(datos, start_date, end_date)
    # datos_filtrados = datos_filtrados[datos_filtrados['operacion'] == value]
    if 'RECIBO' in value:
        datos_filtrados = nsv_recibo_remitente(datos_filtrados)
    elif 'DESPACHO' in value:
        datos_filtrados = nsv_despacho_remitente(datos_filtrados)
    else:
        # Espacio para crear el filtro de 'ENTREGA'
        pass
    trace =[go.Pie(labels=datos_filtrados.columns.values,
                            values=[np.sum(datos_filtrados[empresa]) for empresa in datos_filtrados.columns],
                            hoverinfo='percent',
                            textinfo='label+value',
                            textfont=dict(size=13),
                            hole=.5,
                            rotation=45,
                            textposition='outside')]
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

if __name__ == '__main__':
    app.run_server(debug=True)
