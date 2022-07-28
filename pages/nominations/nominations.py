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
from components.date_picker_range import make_date_picker_range
from utils.functions import load_data
from utils.constants import nominations_data, balance_data

data = load_data(balance_data)

layout = html.Div([
    html.Div([
        make_dash_button("Subir nominaciones", type_button="upload"),
        make_dash_button("Descargar Info Nominaciones", type_button="download")
    ], className='button-container'),
    html.Div([
        html.Div([
             html.P(id="files-to-process-nominations"),
             html.P(id='downloaded-report-nomination'),
        ], className='create_container twelve columns'),
    ], className='row flex-container'),
    html.Div([
        html.Div([
            html.H2("Periodo de Análisis"),
            make_date_picker_range("nomination-period", data),
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
        # Filtrar data según el tipo de operación (entrega, recibo, despacho)
    html.Div([
            dcc.Graph(id="production-factor"),
        ], className="create_container twelve columns"),
    # Contenedor para generar el filtro sobre el tipo de crudo
    
])