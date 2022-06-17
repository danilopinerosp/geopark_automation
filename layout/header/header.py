from dash import html

top_header = html.Div([
        # Contenedor para el logo de Geopark
 #       html.Div([
  #          html.Img(src=app.get_asset_url('logo_geopark.png'),
   #                  id='logo_geopark',
    #                 style={
     #                    "height": "100px",
      #                   "width": "auto",
       #                  "margin-bottom": "25px",
        #             },
         #            )
     #   ],
     #       className="one-third column",
      #  ),
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

nav_menu = html.Div