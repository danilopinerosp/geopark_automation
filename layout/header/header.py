from dash import html, dcc
import dash_bootstrap_components as dbc

from utils.constants import (balance_page_location,
                            nominations_page_location,
                            reports_page_location,
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
            html.H6(f"Última actualización: {1}"),

        ], id="last-update"),

    ], id="top-header", className="row flex-display", style={"margin-bottom": "25px"})

header = html.Div([
    top_header, 
    # Tabs de la aplicación
    dbc.Nav([
            dbc.NavLink("Balance", href=balance_page_location, active="exact", className="nav-menu-item"),
            dbc.NavLink("Nominations", href=nominations_page_location, active="exact", className="nav-menu-item"),
            dbc.NavLink("Reports", href=reports_page_location, active="exact", className="nav-menu-item"),
            dbc.NavLink("Upload", href=upload_page_location, active="exact", className="nav-menu-item"),
        ],
        vertical=False,
        pills=True,
        id="nav-menu"),
], id="header")