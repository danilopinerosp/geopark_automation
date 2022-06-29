from dash import (Dash, 
                Input, 
                Output, 
                callback, 
                dash_table,
                html, 
                dcc)
import pandas as pd

layout = html.Div([
    html.Div([
        html.H2("Dashboard Balance", style={"textAlign": "left"})
    ]),
    html.Div([
        html.H2("Mes",
                    className='fix_label',
                    style={'color':'white', 'text-align':'center'}),
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
                    className='fix_label',
                    style={'color':'white', 'text-align':'center'}),
            dcc.Dropdown(options=['GEOPARK', 'VERANO'],
                        value='GEOPARK', 
                        clearable=False,
                        id='remitente-nominacion',
                        multi=False),
            dcc.Graph(id="factor-servicio"),
        ], className="create_container twelve columns"),
    # Contenedor para generar el filtro sobre el tipo de crudo
    
])