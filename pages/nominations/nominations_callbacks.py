from dash import dcc, callback_context, Input, Output, State
from matplotlib.cbook import report_memory
import plotly.graph_objs as go

# Librerías para el tratamiento de datos
import numpy as np
import pandas as pd

from dash import html

from components.nominations_graph import graph_nominations_results
from pages.balance.balance_data import remove_entries_balance
from pages.nominations.tabs.tigana import tigana_nominations
from pages.nominations.tabs.livianos import livianos_nominations

from app import app

from components.nominations_graph import graph_production_factor

from pages.nominations.nominations_data import daily_transported_oil_type, parse_contents, remove_entries_nominations

from utils.constants import balance_data, header_nominations, nominations_processed, nominations_data
from utils.functions import load_data, log_processed, verify_processed

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

@app.callback(Output("files-to-process-nominations", "children"),
            [Input("subir-nominaciones", 'contents')],
            [State('subir-nominaciones', 'filename'),
            State('subir-nominaciones', 'last_modified')])
def update_daily_reports(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = list()
        # Nombres de los valores a guardar en el balance
        header = header_nominations
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
                df = parse_contents(c, n, d, header)
                # print(df)
                try:

                        if verify_processed(n, nominations_processed):
                                new_data = remove_entries_nominations(nominations_data, n)
                                new_data.to_csv(nominations_data, index=False)
                        else:
                                log_processed(n, nominations_processed, ["fecha actualizacion", "fecha reporte"], "reporte")

                        df.to_csv(nominations_data, "a", header=False, index=False)
                        children.append(html.P(n))
                except Exception as e:
                        children.append(html.Div(['There was an error processing this file.']))

        return children



# Callback to download nominations report
# Callback for downloading button
@app.callback(Output("downloaded-report-nomination", "children"),
            [Input("descargar-info-nominaciones", "n_clicks"),
            Input("nomination-period", "start_date"),
            Input("nomination-period", "end_date")])
def download_report_nomination(n_clicks, start_date, end_date):
        df = load_data(balance_data)
        transported = daily_transported_oil_type(df, start_date, end_date)

        report_name = "kjkh"

        if callback_context.triggered[0]['prop_id'] == "descargar-info-nominaciones.n_clicks":
                transported.to_excel("../ReportesMensuales/Nominaciones/nominacion.xlsx")
                return html.P(f'Se ha descargado el archivo: { report_name }')
