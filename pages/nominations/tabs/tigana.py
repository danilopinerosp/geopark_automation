from components.nominations_graph import graph_nominations_results
import numpy as np
import plotly.graph_objs as go
from dash import dcc

def tigana_nominations():
    # Generación datos Dummi
    y_geopark = np.random.rand(30)* 100
    y_verano = 100 - y_geopark

    data = [
        {
                "companie": "Geopark",
                "transported": y_geopark,
                "nominated": y_geopark,
                "dates": np.arange(0, 30)

        },
        {
                "companie": "Verano",
                "transported": y_verano,
                "nominated": y_verano,
                "dates": np.arange(0, 30)

        }
    ]
    # Generación colores dummi
    colors = ["blue", "orange"]

    return graph_nominations_results(data, colors, "% Tigana", type_graph="Tigana")