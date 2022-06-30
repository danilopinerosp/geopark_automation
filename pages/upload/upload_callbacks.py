from app import app
from dash.dependencies import Input, Output, State

import pandas as pd

from utils.constants import companies
from components.table import make_dash_table

@app.callback(Output("table-data-companies", "children"),
            Input("add-company", "n_clicks"),
            State("add-company-input", "value"))
def render_table_new_companie(n_clicks, value):

    if value != "":
        new_company = pd.DataFrame({"Empresa": [value]})
        new_company.to_csv(companies, mode='a', index=False, header=False)
    
    data_companies = pd.read_csv(companies)

    return make_dash_table(data_companies)