# import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

from app import app

from utils.constants import (balance_page_location, 
                            nominations_page_location, 
                            reports_page_location, 
                            upload_page_location)

from pages.balance import balance
from pages.nominations import nominations
from pages.reports import reports
from pages.upload import upload

from pages.balance.balance_callbacks import *
from pages.nominations.nominations_callbacks import *
from pages.reports.reports_callbacks import *
from pages.upload.upload_callbacks import *

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    print("PATHNAME: ", pathname)
    if pathname == balance_page_location:
        return balance.layout
    elif pathname == nominations_page_location:
        return nominations.layout
    elif pathname == reports_page_location:
        return reports.layout
    elif pathname == upload_page_location:
        return upload.layout
    return balance.layout
    #return html.Div([
    #    html.H1("404: Not found", className="text-danger"),
    #    html.Hr(),
    #    html.P(f"The pathname {pathname} was not recognized")
    #])