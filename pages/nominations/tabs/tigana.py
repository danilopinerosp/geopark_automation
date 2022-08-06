from tracemalloc import start
from components.nominations_graph import graph_nominations_results
import numpy as np
import plotly.graph_objs as go
from dash import dcc

from pages.nominations.nominations_data import get_data_percentage_nominations

def tigana_nominations(data, start_date, end_date):
    # Generación datos Dummi
    y_geopark = np.random.rand(30)* 100
    y_verano = 100 - y_geopark

    data_tigana = get_data_percentage_nominations(start_date, end_date, 'Tigana')
    print(data_tigana)
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