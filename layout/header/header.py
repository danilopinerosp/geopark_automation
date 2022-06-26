from dash import html, dcc
import dash_bootstrap_components as dbc

from utils.constants import (balance_page_location,
                            nominations_page_location,
                            reports_page_location,
                            upload_page_location
                            )

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

top_header = html.Div([
        # Contenedor para el logo de Geopark
        html.Div([
            html.Img(src='./assets/logo_geopark.png',
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
            html.H6(f"Última actualización: {1}",
                    style={'color': 'orange'}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"})

header = html.Div([
    top_header, 
    # Tabs de la aplicación
    dbc.Nav([
            dbc.NavLink("Balance", href=balance_page_location, active="exact"),
            dbc.NavLink("Nominations", href=nominations_page_location, active="exact"),
            dbc.NavLink("Reports", href=reports_page_location, active="exact"),
            dbc.NavLink("Upload", href=upload_page_location, active="exact"),
        ],
        vertical=False,
        pills=True,
        style=tabs_styles),
])