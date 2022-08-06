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
    data = list()
    for name_company in data_tigana:
        data.append({
            'companie': name_company.capitalize(),
            'transported': data_tigana[name_company][1].iloc[:, 1],
            'nominated': data_tigana[name_company][0].iloc[:, 1],
            'dates': data_tigana[name_company][0]['fecha']
        })

    # Generación colores dummi
    colors = {'geopark': '#FC7637', 'parex': '#137ED2'}
    print(data)

    return graph_nominations_results(data, colors, "% Tigana", type_graph="Tigana")