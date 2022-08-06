from components.nominations_graph import graph_nominations_results
import numpy as np
import plotly.graph_objs as go
from dash import dcc

from pages.nominations.nominations_data import get_data_percentage_nominations

def livianos_nominations(data, start_date, end_date):
    data_livianos = get_data_percentage_nominations(start_date, end_date, 'Livianos')

    total_transported = 0
    total_nominated = 0

    for name_company in data_livianos:
        total_transported += data_livianos[name_company][1].iloc[:, 1]
        total_nominated += data_livianos[name_company][0].iloc[:, 1]

    data = list()
    for name_company in data_livianos:
        data.append({
            'companie': name_company.capitalize(),
            'transported': (data_livianos[name_company][1].iloc[:, 1]) / total_transported,
            'nominated': (data_livianos[name_company][0].iloc[:, 1]) / total_nominated,
            'dates': data_livianos[name_company][0]['fecha']
        })

    # Generación colores dummi
    colors = {'geopark': '#FC7637', 'parex': '#137ED2'}
    print(data)

    return graph_nominations_results(data, colors, "% Livianos", type_graph="Livianos")