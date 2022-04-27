from dash import dcc, html

layout_informes = html.Div([
    html.Div([
        html.Div([
            html.H2("Reporte",
                    className='fix_label',
                    style={'color':'white', 'text-align':'center'}),
            dcc.Dropdown(options=['Balance', 'Acta ODCA'],
                        value='Balance',
                        clearable=False,
                        id='tipo-datos',
                        multi=False),
        ], className='create_container four columns'),
        html.Div([
            html.H2("Mes",
                    className='fix_label',
                    style={'color':'white', 'text-align':'center'}),
            dcc.Dropdown(options=['Enero', 'Febrero', 'Marzo', 'Abril'],
                        value='Abril', 
                        clearable=False,
                        id='tipo-datos',
                        multi=False),
        ], className="create_container four columns"),
        html.Button('Generar', id='generar-reporte', n_clicks=0),
    ], className='row flex-display')
], style={'background-color':'#2679CE'})