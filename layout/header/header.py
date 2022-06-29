from dash import html
import dash_bootstrap_components as dbc
from utils.constants import BALANCE_DATA
from layout.header.header_data import get_date_last_update

from utils.constants import (balance_page_location,
                            nominations_page_location,
                            upload_page_location
                            )

top_header = html.Div([
        # Contenedor para el logo de Geopark
        html.Div([
            html.Img(src='./assets/logo_geopark.png', id='logo_geopark'
                    )
        ], id="logo"),
        # Contenedor para el título del dashboard
        html.Div([
            html.H1("Resultados de la operación"),
        ], id="main-title"),
        # Contenedor para la fecha de la última actualización (último reporte contenido
        # en el análisis)
        html.Div([
            html.H6(f"Última actualización: {get_date_last_update(BALANCE_DATA)}"),

        ], id="last-update"),

    ], id="top-header", className="row flex-display", style={"margin-bottom": "25px"})

header = html.Div([
    top_header, 
    # Tabs de la aplicación
    dbc.Nav([
            dbc.NavLink("Balance", href=balance_page_location, active="exact", className="nav-menu-item"),
            dbc.NavLink("Nominaciones", href=nominations_page_location, active="exact", className="nav-menu-item"),
            dbc.NavLink("Datos", href=upload_page_location, active="exact", className="nav-menu-item"),
        ],
        vertical=False,
        pills=True,
        id="nav-menu"),
], id="header")