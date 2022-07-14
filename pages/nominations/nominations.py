from dash import (Dash, 
                Input, 
                Output, 
                callback, 
                dash_table,
                html, 
                dcc)
import pandas as pd
from datetime import datetime as dt

from components.button import make_dash_button

from data.server import datos

layout = html.Div([
    html.Div([
        make_dash_button("Subir nominaciones", type_button="upload"),
        make_dash_button("Descargar Info Nominaciones", type_button="download")
    ], className='button-container'),
    html.Div([
        html.Div([
            html.H2("Periodo de Análisis"),
            dcc.DatePickerRange(
                id='nomination-period',
                # Las fechas mínimas y máximas permitidas dependerán de las fechas
                # de los datos del balance
                min_date_allowed=datos['fecha'].min().to_pydatetime(),
                max_date_allowed=datos['fecha'].max().to_pydatetime(),
                initial_visible_month=dt(datos['fecha'].dt.year.max(),
                                        datos['fecha'].max().to_pydatetime().month, 1),
                # Por defecto toma como periodo de análisis los datos recolectados del último mes.
                start_date=(datos[datos['fecha'].dt.month == datos['fecha'].max().month]['fecha'].min()).to_pydatetime(),
                end_date=datos['fecha'].max().to_pydatetime(),
                display_format='DD/MM/Y'),
            html.H2("Remitente"),
            dcc.Dropdown(options=['GEOPARK', 'VERANO'],
                        value='GEOPARK', 
                        clearable=False,
                        id='remitente-nominacion',
                        multi=False),
            ], className="create_container three columns"),
        html.Div([
        dcc.Tabs(id="tabs-nominations", value='tigana', 
            children=[dcc.Tab(label='Tigana', value='tigana'),
                    dcc.Tab(label='Livianos', value='livianos'),
            ]
        ),
        dcc.Graph(id="graph-nominations-results")
        ], className="create_container nine columns"),
    ], className="row flex-display"),
        # Filtrar datos según el tipo de operación (entrega, recibo, despacho)
    html.Div([
            dcc.Graph(id="production-factor"),
        ], className="create_container twelve columns"),
    # Contenedor para generar el filtro sobre el tipo de crudo
    
])