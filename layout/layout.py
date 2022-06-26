from dash import dcc, html

from layout.header.header import header

content = html.Div(id='page-content')

layout = html.Div([dcc.Location(id="url"), header, content])