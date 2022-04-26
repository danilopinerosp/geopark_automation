from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Librería para trabajar con fechas
from datetime import datetime as dt
from dash import dcc, html
from server import datos

# Importar layout Dashboard Balance
from layouts.layout_balance import layout_balance

# Importar todos los callbacks
from callbacks.visualizations import *
from callbacks.values import *

EMPRESAS = ['GEOPARK', 'PAREX']
CONDICIONES = ['GOV', 'GSV', 'NSV']

# app = Dash(__name__)

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# app.
layout = html.Div([
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
            html.H6(f"Última actualización: {datos['fecha'].max().strftime('%d/%m/%Y')}",
                    style={'color': 'orange'}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),
    # Tabs de la aplicación
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Datos', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Generarión de Informes', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Dashboard Balance', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Dashboard Nominaciones', value='tab-4', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Reportes Diarios')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Generación de Informes')
        ])
    elif tab == 'tab-3':
        return html.Div([
            layout_balance
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Dashboard Nominaciones')
        ])
