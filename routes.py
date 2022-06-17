import dash_bootstrap_components as dbc
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

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == balance_page_location:
        return balance.layout
    elif pathname == nominations_page_location:
        return nominations.layout
    elif pathname == reports_page_location:
        return reports.layout
    elif pathname == upload_page_location:
        return upload.layout
    # If the user tries to reach a page that does not exist, return a 404 page
    else:
