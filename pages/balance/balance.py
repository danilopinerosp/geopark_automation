# Librería para trabajar con fechas
from datetime import datetime as dt
from dash import dcc, html
from components.date_picker_range import make_date_picker_range
from data.functions.database import init_database
from components.button import make_dash_button
from components.cumulated_card import make_cumulated_card
from pages.balance.balance_data import get_date_last_report

from utils.constants import EMPRESAS, CONDICIONES, balance_data
from utils.functions import load_data

init_database()

data = load_data(balance_data)

layout = html.Div([
    # Container for cumulates by company and operation conditions
    html.Div([
        # Containers for Geopark's cumulated in specified period of time
        make_cumulated_card("geopark", "GOV"),
        make_cumulated_card("geopark", "GSV"),
        make_cumulated_card("geopark", "NSV"),  
        # Containers for Parex's cumulated in specified period of time
        make_cumulated_card("parex", "GOV"),
        make_cumulated_card("parex", "GSV"),
        make_cumulated_card("parex", "NSV"),
    ], className="row flex-display"),
    # Container for the buttons to download daily reports and upload balance reports
    html.Div([
        make_dash_button("Subir reporte diario", type_button="upload"),
        make_dash_button("Descargar Acta", type_button="download"),
        html.Div(id="files-to-process")
    ], className='button-container'),

    # Contenedor para la participación de Geopark, le operación del día y la producción
    # histórica
    html.Div([
        # Contenedor para mostrar los resultado de la operación de la fecha más reciente
        # de actualización para Geopark y generar los filtros por fecha y tipo de operación
        html.Div([
            html.H3('Periodo de Análisis'),
            # Permite seleccionar las fechas en las que se quiere realizar el análisis
            make_date_picker_range("balance-period-analysis", data),
            # Filtrar data según el tipo de operación (entrega, recibo, despacho)
            html.H3('Tipo de Operación a analizar'),
            dcc.Dropdown(options=data['operacion'].unique(),
                        value='RECIBO POR REMITENTE TIGANA',
                        clearable=False,
                        id='tipo-operacion',
                        multi=False),
            html.H3(f"Operación Geopark"),
            html.H4(f"{get_date_last_report(data)}"),
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
            html.H3(id="title-cumulated"),
            dcc.Graph(id='graph-cumulated'),
        ], className='create_container six columns'),
        html.Div([
            html.H3(id="title-inventory"),
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
        # Filtrar data según el tipo de operación (entrega, recibo, despacho)
    ], className='row flex-display'),
    # Contenedor para generar el filtro sobre el tipo de crudo
    html.Div([
        dcc.RadioItems(options=CONDICIONES,
            value='NSV',
            id='condiciones-operacion',
            inline=True)
        ], style={'text-align':'center'})
], id='mainContainer', style={'display':'flex', 'flex-direction':'column'})