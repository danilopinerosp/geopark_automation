from dash.dependencies import Input, Output
from dash import html
from app import app

from pages.balance import balance
from pages.nominations import nominations
from pages.reports import reports
from pages.upload import upload


@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return upload.layout
    elif tab == 'tab-2':
        return reports.layout
    elif tab == 'tab-3':
        return balance.layout
    elif tab == 'tab-4':
        return nominations.layout