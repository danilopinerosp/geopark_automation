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


def graph_accomplishment_factor(type_oils_nominations, type_oils_transported, colors, title_graph, data_nominated, data_transported):
    trace = list()
    for column_name in data_transported.columns[1:]:
        trace.append(go.Bar(x=data_transported['fecha'],
                                    y=data_transported[column_name],
                                    textposition='auto',
                                    name=f"{type_oils_transported[column_name]} Transportado",
                                    marker={"color":colors[type_oils_transported[column_name]]}))
        
    for column_name in data_nominated.columns[1:]:
        trace.append(go.Scatter(x=data_nominated['fecha'],
                                    y=data_nominated[column_name], 
                                    name=f"{type_oils_nominations[column_name]} Nominado",
                                    line={'width':3, 'color':colors[type_oils_nominations[column_name]]}),
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
                                    xanchor='center', x= 0.5, y= -0.1),
                        height=600

                        )

    return {'data':trace, 'layout':layout}