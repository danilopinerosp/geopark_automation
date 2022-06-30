from dash import (Dash, 
                Input, 
                Output, 
                callback, 
                dash_table,
                html, 
                dcc)
import pandas as pd

from components.button import make_dash_button

layout = html.Div([
    html.Div([
        make_dash_button("Subir nominaciones", type_button="upload"),
        make_dash_button("Descargar Info Nominaciones", type_button="download")
    ], className='button-container'),
    html.Div([
        html.H2("Mes"),
        dcc.Dropdown(options=['Enero', 'Febrero', 'Marzo', 'Abril'],
                        value='Abril', 
                        clearable=False,
                        id='mes-nominacion',
                        multi=False),
    ]),
    html.Div([
        dcc.Tabs(id="tabs-nominations", value='tigana', 
            children=[dcc.Tab(label='Tigana', value='tigana'),
                    dcc.Tab(label='Livianos', value='livianos'),
            ]
        ),
        dcc.Graph(id="graph-nominations-results")
    ], className="tabs-container"),
        # Filtrar datos según el tipo de operación (entrega, recibo, despacho)
    html.Div([
            html.H2("Remitente",
                    className='fix_label'),
            dcc.Dropdown(options=['GEOPARK', 'VERANO'],
                        value='GEOPARK', 
                        clearable=False,
                        id='remitente-nominacion',
                        multi=False),
            dcc.Graph(id="production-factor"),
        ], className="create_container twelve columns"),
    # Contenedor para generar el filtro sobre el tipo de crudo
    
])