# Librería para trabajar con fechas
from datetime import datetime as dt
from dash import dcc, html
from data.server import datos
from components.button import make_dash_button

from utils.constants import EMPRESAS, CONDICIONES

layout = html.Div([
    # Contenedor donde se ubicaran los 6 acumulados por tipo de crudo para las dos empresas
    html.Div([
        # Contenedor GOV cumulado por tipo de operación en el periodo indicado de Geopark
        html.Div([
            html.H6(children='Geopark GOV (bbls)'),
            html.P(id='GOV-acumulado-geopark'
                   )], className="card_container two columns acumulado-geopark",
        ),
        # Contenedor GSV cumulado por tipo de operación en el periodo indicado de Geopark
        html.Div([
            html.H6(children='Geopark GSV (bbls)'),

            html.P(id='GSV-acumulado-geopark'
                   )], className="card_container two columns acumulado-geopark",
        ),
        # Contenedor NSV cumulado por tipo de operación en el periodo indicado de Geopark
        html.Div([
            html.H6(children='Geopark NSV (bbls)'),

            html.P(id='NSV-acumulado-geopark'
                   )], className="card_container two columns acumulado-geopark",
        ),
        # Contenedor GOV cumulado por tipo de operación en el periodo indicado de Parex
        html.Div([
            html.H6(children='Parex GOV (bbls)'),

            html.P(id='GOV-acumulado-parex'
                   )], className="card_container two columns acumulado-parex"),
        # Contenedor GSV cumulado por tipo de operación en el periodo indicado de Parex
        html.Div([
            html.H6(children='Parex GSV (bbls)'),

            html.P(id='GSV-acumulado-parex'
                   )], className="card_container two columns acumulado-parex"),
        # Contenedor NSV cumulado por tipo de operación en el periodo indicado de Parex
        html.Div([
            html.H6(children='Parex NSV (bbls)'),

            html.P(id='NSV-acumulado-parex'
                   )], className="card_container two columns acumulado-parex")

    ], className="row flex-display"),
    # Container for the buttons to download daily reports and upload balance reports
    html.Div([
        make_dash_button("Subir reporte diario", type_button="upload"),
        make_dash_button("Descargar Acta", type_button="download")
    ], className='button-container'),

    # Contenedor para la participación de Geopark, le operación del día y la producción
    # histórica
    html.Div([
        # Contenedor para mostrar los resultado de la operación de la fecha más reciente
        # de actualización para Geopark y generar los filtros por fecha y tipo de operación
        html.Div([
            html.H3('Periodo de Análisis'),
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
                start_date=(datos[datos['fecha'].dt.month == datos['fecha'].max().month]['fecha'].min()).to_pydatetime(),
                end_date=datos['fecha'].max().to_pydatetime(),
                display_format='DD/MM/Y'
            ),
            # Filtrar datos según el tipo de operación (entrega, recibo, despacho)
            html.H3('Tipo de Operación a analizar'),
            dcc.Dropdown(options=datos['operacion'].unique(),
                        value='RECIBO POR REMITENTE TIGANA',
                        clearable=False,
                        id='tipo-operacion',
                        multi=False),
            html.H3(f"Operación Geopark"),
            html.H4(f"{datos['fecha'].max().strftime('%d/%m/%Y')}"),
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
            html.H3(id="title-participaction-company"),
            dcc.Graph(id='participacion-empresa',
                    config={'displayModeBar':'hover'})
        ], className='create_container four columns'),
        
        # Contenedor para graficar la producción histórica por tipo de empresa y condición
        # de operación
        html.Div([
            html.H3(id="title-historical-nsv"),
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
            ], style={'text-align':'center'})
        ], className='create_container six columns'),
        # Filtrar datos según el tipo de operación (entrega, recibo, despacho)
    ], className='row flex-display'),
    # Contenedor para generar el filtro sobre el tipo de crudo
    html.Div([
        dcc.RadioItems(options=CONDICIONES,
            value='NSV',
            id='condiciones-operacion',
            inline=True)
        ], style={'text-align':'center'})
], id='mainContainer', style={'display':'flex', 'flex-direction':'column'})