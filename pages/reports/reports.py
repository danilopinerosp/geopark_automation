from dash import dcc, html

layout = html.Div([
    html.Div([
        html.Div([
            html.H2("Reporte",
                    className='fix_label',
                    style={'color':'white', 'text-align':'center'}),
            dcc.Dropdown(options=['Nominaciones', 'Acta ODCA'],
                        value='Acta ODCA',
                        clearable=False,
                        id='tipo-reporte',
                        multi=False),
        ], className='create_container four columns'),
        html.Div([
            html.H2("Mes",
                    className='fix_label',
                    style={'color':'white', 'text-align':'center'}),
            dcc.Dropdown(options=['Enero', 'Febrero', 'Marzo', 'Abril', "Mayo"],
                        value='Abril', 
                        clearable=False,
                        id='mes-reporte',
                        multi=False),
        ], className="create_container four columns"),
        html.Button('Descargar Informe', id='boton-informe'),
        dcc.Download(id="descargar-informe")
    ], className='row flex-display')
], style={'background-color':'#2679CE'})