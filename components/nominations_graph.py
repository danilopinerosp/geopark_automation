import plotly.graph_objs as go
from dash import dcc

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