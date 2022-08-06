from tracemalloc import start
from components.nominations_graph import graph_nominations_results
import numpy as np
import plotly.graph_objs as go
from dash import dcc

from pages.nominations.nominations_data import get_data_percentage_nominations

def tigana_nominations(data, start_date, end_date):

    data_tigana = get_data_percentage_nominations(start_date, end_date, 'Tigana')

    total_transported = 0
    total_nominated = 0

    for name_company in data_tigana:
        total_transported += data_tigana[name_company][1].iloc[:, 1]
        total_nominated += data_tigana[name_company][0].iloc[:, 1]

    data = list()
    for name_company in data_tigana:
        data.append({
            'companie': name_company.capitalize(),
            'transported': (data_tigana[name_company][1].iloc[:, 1] / total_transported) * 100,
            'nominated': (data_tigana[name_company][0].iloc[:, 1] / total_nominated ) * 100,
            'dates': data_tigana[name_company][0]['fecha']
        })

    # Generación colores dummi
    colors = {'geopark': '#FC7637', 'parex': '#137ED2'}
    return graph_nominations_results(data, colors, "% Tigana", type_graph="Tigana")