from dash import dcc, html

from layout.header.header import header

content = html.Div(id='tabs-content-inline')

layout = html.Div([dcc.Location(id="url"), header, content])