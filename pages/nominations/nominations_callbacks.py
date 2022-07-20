from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Librerías para el tratamiento de datos
import numpy as np
import pandas as pd

from dash import html

from components.nominations_graph import graph_nominations_results
from pages.nominations.tabs.tigana import tigana_nominations
from pages.nominations.tabs.livianos import livianos_nominations

from app import app

from components.nominations_graph import graph_production_factor

from pages.nominations.nominations_data import daily_transported_oil_type

@app.callback(Output("graph-nominations-results", component_property="figure"),
        Input("tabs-nominations", "value"))
def render_tabs_nominations(tab):
        if tab == "tigana":
                return tigana_nominations()
        elif tab == "livianos":
                return livianos_nominations()

@app.callback(Output("production-factor", component_property="figure"),
            [Input("nomination-period", "start_date"),
            Input("nomination-period", "end_date"),
            Input("remitente-nominacion", "value")])
def actualizar_factor_servicio(start_date, end_date, remitente):

    # Generación datos Dummi
    type_oils = ["Jacana", "Tigana", "Livianos", "Cabrestero"]
    # Generación colores dummi
    colors = {"Jacana":"orange", "Tigana": "blue", "Livianos": "grey", "Cabrestero": "green"}

    title_graph = f"""
    Factor de Cumplimiento<br>
    Mes: {start_date}<br>
    Remitente: {remitente}
    """

    return graph_production_factor(type_oils, colors, title_graph)

# Callback to download nominations report
# Callback for downloading button
@app.callback(Output("descargar-info-nominaciones", "data"),
            [Input("descargar-info-nominaciones-button", "n_clicks"),
            Input("nomination-period", "start_date"),
            Input("nomination-period", "end_date")],
            prevent_initial_call=True,)
def descargar_informe(n_clicks, start_date, end_date):
    df = pd.read_csv("data/consolidated_data/balance.csv")
    transported = daily_transported_oil_type(df, start_date, end_date)
    if n_clicks > 0:
        return dcc.send_data_frame(transported.to_excel, f"nominaciones.xlsx", 
                                sheet_name="Consolidado Nominaciones")  

    