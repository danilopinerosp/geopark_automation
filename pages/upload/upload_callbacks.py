from app import app
from dash.dependencies import Input, Output, State

import pandas as pd

from utils.constants import companies, oils
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

@app.callback(Output("table-oil-types", "children"),
            Input("add-oil", "n_clicks"),
            State("add-oil-input", "value"),
            State("add-segment-input", "value"))
def render_table_oil_types(n_clicks, oil_name, segment_number):
    if oil_name != "" and segment_number != "":
        new_oil = pd.DataFrame({
                                "Crudo": [oil_name], 
                                "Segmento": [segment_number]})
        new_oil.to_csv(oils, mode="a", index=False, header=False)
    
    data_oils = pd.read_csv(oils)
    
    return make_dash_table(data_oils)