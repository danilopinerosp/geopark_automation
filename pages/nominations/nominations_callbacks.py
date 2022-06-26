from dash import dcc
from dash import callback_context
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Librerías para el tratamiento de datos
import numpy as np
import pandas as pd


from data.server import datos  #Line must be remove with the new architecture
from app import app


# callback para actualizar tigana-transportado
@app.callback(Output("tigana-transportado", component_property="figure"),
            Input("mes-nominacion", "value"))
def actualizar_tigana_transportado(mes):
    # Generación datos Dummi
    y_geopark = np.random.rand(30)* 100
    y_verano = 100 - y_geopark
    # Generación colores dummi
    colores = ["red", "grey"]

    trace = [go.Bar(x=np.arange(0, 30),
                    y=y_geopark,
                    textposition='auto',
                    name="% Transportado Tigana Geopark",
                    marker={"color": colores[0]}),
            go.Bar(x=np.arange(0, 30),
                    y=y_verano,
                    textposition='auto',
                    name="% Transportado Tigana Verano",
                    marker={"color": colores[1]}),
            go.Scatter(x=np.arange(0, 30),
                    y=y_geopark, 
                    name="% Nominado Tigana Geopark",
                    line={'width':3, 'color':colores[0]}),
            go.Scatter(x=np.arange(0, 30),
                    y=y_verano,
                    name="% Nominado Tigana Verano",
                    line={'width':3, 'color':colores[1]})]

    layout = go.Layout(title={'text': "% Tigana",
                                'y':0.93,
                                'x':0.5,
                                'xanchor':'center',
                                'yanchor':'top'},
                        titlefont={'color': 'white', 'size': 20},
                        font=dict(color='white'),
                        paper_bgcolor='#1f2c56',
                        plot_bgcolor='#1f2c56',
                        legend=dict(orientation="h",
                                    yanchor="bottom",
                                    xanchor='center', x= 0.5, y= -0.2   )
                        )
    return {'data':trace, 'layout':layout}


@app.callback(Output("livianos-transportado", component_property="figure"),
            Input("mes-nominacion", "value"))
def actualizar_livianos_transportado(mes):
    # Generación datos Dummi
    y_geopark = np.random.rand(30)* 100
    y_verano = 100 - y_geopark
    # Generación colores dummi
    colores = ['red', 'grey']

    trace = [go.Bar(x=np.arange(0, 30),
                    y=y_geopark,
                    textposition='auto',
                    name="% Livianos Transportado Geopark",
                    marker={"color":colores[0]}),
            go.Bar(x=np.arange(0, 30),
                    y=y_verano,
                    textposition='auto',
                    name="% Livianos transportaos Verano",
                    marker={"color":colores[1]}),
            go.Scatter(x=np.arange(0, 30),
                    y=y_geopark, 
                    name="% Livianos Nominado Geopark",
                    line={'width':3, 'color':colores[0]}),
            go.Scatter(x=np.arange(0, 30),
                    y=y_verano,
                    name="% Livianos Nominado Verano",
                    line={'width':3, 'color':colores[1]})]

    layout = go.Layout(title={'text': "Nominación Livianos",
                                'y':0.93,
                                'x':0.5,
                                'xanchor':'center',
                                'yanchor':'top'},
                        titlefont={'color': 'white', 'size': 20},
                        font=dict(color='white'),
                        paper_bgcolor='#1f2c56',
                        plot_bgcolor='#1f2c56',
                        legend=dict(orientation="h",
                                    yanchor="bottom",
                                    xanchor='center', x= 0.5, y= -0.2   )
                        )
    return {'data':trace, 'layout':layout}

@app.callback(Output("factor-servicio", component_property="figure"),
            [Input("mes-nominacion", "value"),
            Input("remitente-nominacion", "value")])
def actualizar_factor_servicio(mes, remitente):
    # Generación datos Dummi
    tipos = ["Jacana", "Tigana", "Livianos", "Cabrestero"]
    # Generación colores dummi
    colores = {"Jacana":"orange", "Tigana": "blue", "Livianos": "grey", "Cabrestero": "green"}
    trace = list()
    for tipo in tipos:
        y_simulado = np.random.rand(30)* 100
        trace.append(go.Bar(x=np.arange(0, 30),
                                y=y_simulado,
                                textposition='auto',
                                name=f"{tipo} Transportado",
                                marker={"color":colores[tipo]}))
        trace.append(go.Scatter(x=np.arange(0, 30),
                                y=y_simulado, 
                                name=f"{tipo} Transportado",
                                line={'width':3, 'color':colores[tipo]}),
                    )

    title_graph = f"""
    Factor de Servicio<br>
    Mes: {mes}<br>
    Remitente: {remitente}
    """

    layout = go.Layout(title={'text': title_graph,
                                'y':0.93,
                                'x':0.5,
                                'xanchor':'center',
                                'yanchor':'top'},
                        titlefont={'color': 'white', 'size': 20},
                        font=dict(color='white'),
                        paper_bgcolor='#1f2c56',
                        plot_bgcolor='#1f2c56',
                        legend=dict(orientation="h",
                                    yanchor="bottom",
                                    xanchor='center', x= 0.5, y= -0.5   )
                        )
    return {'data':trace, 'layout':layout}