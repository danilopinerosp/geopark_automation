from dash import (Dash, 
                Input, 
                Output, 
                callback, 
                dash_table,
                html, 
                dcc)
import pandas as pd

layout_nominaciones = html.Div([
     html.Div([
        html.Div([
            dcc.Graph(id='nominaciones1-empresa'),
        ], className='create_container six columns'),
        html.Div([
            dcc.Graph(id='nominaciones2-empresa'),
        ], className='create_container six columns'),
        # Filtrar datos según el tipo de operación (entrega, recibo, despacho)
    ], className='row flex-display'),
    html.Div([
            html.H2("Mes",
                    className='fix_label',
                    style={'color':'white', 'text-align':'center'}),
            dcc.Dropdown(options=['Enero', 'Febrero', 'Marzo', 'Abril'],
                        value='Abril', 
                        clearable=False,
                        id='mes_nominacion',
                        multi=False),
            html.H2("Remitente",
                    className='fix_label',
                    style={'color':'white', 'text-align':'center'}),
            dcc.Dropdown(options=['GEOPARK', 'VERANO'],
                        value='GEOPARK', 
                        clearable=False,
                        id='remitente-nominacion',
                        multi=False),
            dcc.Graph(id="factor_servicio"),
        ], className="create_container eleven columns"),
    # Contenedor para generar el filtro sobre el tipo de crudo
    
])