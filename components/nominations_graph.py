import plotly.graph_objs as go

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


def graph_accomplishment_factor(type_oils, colors, title_graph, data_nominated, data_transported):
    trace = list()
    for oil_type, column_name in zip(type_oils, data_nominated.columns):
        trace.append(go.Bar(x=data_nominated['fecha'],
                                    y=data_nominated[column_name],
                                    textposition='auto',
                                    name=f"{oil_type} Nominado",
                                    marker={"color":colors[oil_type]}))
        
    for oil_type, column_name in zip(type_oils, data_transported.columns):
        trace.append(go.Scatter(x=data_transported['fecha'],
                                    y=data_transported[column_name], 
                                    name=f"{oil_type} Transportado",
                                    line={'width':3, 'color':colors[oil_type]}),
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