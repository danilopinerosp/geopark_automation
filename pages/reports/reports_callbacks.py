from app import app

from dash import dcc
from dash import callback_context
from dash.dependencies import Input, Output
import plotly.graph_objs as go
# Librerías para el tratamiento de datos
import numpy as np
import pandas as pd

from data.server import datos

@app.callback(Output("descargar-informe", "data"),
            [Input("boton-informe", "n_clicks"),
            Input("mes-reporte", "value"),
            Input("tipo-reporte", "value")],
            prevent_initial_call=True,)
def descargar_informe(n_clicks, mes, reporte):
    # Generar datos dummies a descargar
    df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 1, 5, 6], "c": ["x", "x", "y", "y"]})
    if n_clicks > 0:
        return dcc.send_data_frame(df.to_excel, f"{reporte} - {mes}.xlsx", sheet_name=reporte)