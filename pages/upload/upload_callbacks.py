from app import app
from dash import Input, Output, State, callback_context

import pandas as pd

from utils.constants import companies, oils
from components.table import make_dash_table

@app.callback(Output("table-data-companies", "children"),
            [Input("add-company", "n_clicks"),
            Input('delete-company', 'n_clicks')],
            State("add-company-input", "value"))
def render_table_new_companie(n_clicks_add, n_clicks_del, company_name):
    data_companies = pd.read_csv(companies)
    if 'add-company.n_clicks' == callback_context.triggered[0]['prop_id']:
        if company_name:
            new_company = pd.DataFrame({"Nombre": [company_name.upper()]})
            new_company.to_csv(companies, mode="a", index=False, header=False)
    if 'delete-company.n_clicks' == callback_context.triggered[0]['prop_id']:
        data_companies = pd.read_csv(companies)
        data_companies = data_companies[data_companies['Nombre'] != company_name.upper()]
        data_companies.to_csv(companies, mode="w", index=False, header=True)
    
    return make_dash_table(companies)

@app.callback(Output("table-oil-types", "children"),
            [Input("add-oil", "n_clicks"),
            Input("delete-oil", "n_clicks")],
            State("add-oil-input", "value"),
            State("add-livianos-input", "value"))
def render_table_oil_types(n_clicks_add, n_clicks_del, oil_name, segment_number):
    if 'add-oil.n_clicks' == callback_context.triggered[0]['prop_id']:
        if oil_name and segment_number:
            new_oil = pd.DataFrame({"Crudo": [oil_name.upper()], "Livianos": [segment_number.upper()]})
            new_oil.to_csv(oils, mode="a", index=False, header=False)
    if 'delete-oil.n_clicks' == callback_context.triggered[0]['prop_id']:
        data_oils = pd.read_csv(oils)
        data_oils = data_oils[data_oils['Crudo'] != oil_name.upper()]
        data_oils.to_csv(oils, mode="w", index=False, header=True)
    
    return make_dash_table(oils)