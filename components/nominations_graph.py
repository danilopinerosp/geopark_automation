import plotly.graph_objs as go
import numpy as np
from utils.constants import nominations_data

def graph_nominations_results(data, colors, title, type_graph="Tigana"):

    trace = []
    dates = data[0]['dates']

    for idx, i in enumerate(data):
        trace.append(
            go.Bar(x=dates,
                    y=i['transported'],
                    textposition='auto',
                    name=f"% Transportado { i['companie'] }",
                    marker={"color": colors[idx]}),
        )
        trace.append(
            go.Scatter(x=dates,
                    y=i['nominated'], 
                    name=f"% Nominado { i['companie'] }",
                    line={'width': 3, 'color':colors[idx]}),
        )

    layout = go.Layout(title={'text': title,
                                'y':0.93,
                                'x':0.5,
                                'xanchor':'center',
                                'yanchor':'top'},
                        titlefont={'size': 20},
                        font=dict(color='#262830'),
                        paper_bgcolor='#f3f3f3',
                        plot_bgcolor='#f3f3f3',
                        legend=dict(orientation="h",
                                    yanchor="bottom",
                                    xanchor='center', x= 0.5, y= -0.2   )
                        )
    return {'data':trace, 'layout':layout}


def graph_accomplishment_factor(type_oils, colors, title_graph, data):
    print(data)
    trace = list()
    for t in type_oils:
        y_simulado = np.random.rand(30)* 100
        trace.append(go.Bar(x=np.arange(0, 30),
                                y=y_simulado,
                                textposition='auto',
                                name=f"{t} Transportado",
                                marker={"color":colors[t]}))
        trace.append(go.Scatter(x=np.arange(0, 30),
                                y=y_simulado, 
                                name=f"{t} Transportado",
                                line={'width':3, 'color':colors[t]}),
                    )

    layout = go.Layout(title={'text': title_graph,
                                'y':0.93,
                                'x':0.5,
                                'xanchor':'center',
                                'yanchor':'top'},
                        titlefont={'color': '#262830', 'size': 20},
                        font=dict(color='#262830'),
                        paper_bgcolor='#f3f3f3',
                        plot_bgcolor='#f3f3f3',
                        legend=dict(orientation="h",
                                    yanchor="bottom",
                                    xanchor='center', x= 0.5, y= -0.5   )
                        )
    return {'data':trace, 'layout':layout}