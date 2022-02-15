import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from obtener_datos import CONDICIONES

from procesar_datos import total_crudo, total_crudo_empresa

# Cargos los datos del balance
datos = pd.read_csv('balance.csv')
# Convertir las fechas al tipo de dato datatime
datos['fecha'] = pd.to_datetime(datos['fecha'], dayfirst=True)

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

            html.P(f"{total_entrega:,.2f}", # formatea el valor a 3 decimales
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
    html.Div([
        # Contenedor para crear el filtro por condicione de operación y mostrar los resultados del último día
        html.Div([
            # Filtrar datos según las condicione de operación
            html.P('Condiciones de Operación:', className='fix_label', style={'color':'white'}),
            dcc.Dropdown(options=CONDICIONES,
                        value='NSV',
                        clearable=False,
                        id='cond_operacion',
                        multi=False),
            html.P(f"Resultados Operación: {datos['fecha'].iloc[-1].strftime('%d/%m/%Y')}",
                    className='fix_label', style={'color':'white', 'text-align':'center'})
        ], className='create_container three columns', id='cross-filter-options'), 
        # Contenedor para graficar la participación en la producción por empresa (según la condición elegida)
        html.Div([
            dcc.Graph(id='pie_chart',
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
            [dcc.Graph(id='bar_chart')
        ], className='create_container1 twelve columns')
    ], className='row flex-display')
], id='mainContainer', style={'display':'flex', 'flex-direction':'column'})

if __name__ == '__main__':
    app.run_server(debug=True)
