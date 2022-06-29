import plotly.graph_objs as go

def graph_indicator(data, previous_data, color):
    """
    Graph indicator according to production data and previous production data
    """
    indicator = [go.Indicator(
                        mode='number+delta',
                        value=data,
                        delta={'reference':previous_data,
                                'position':'right',
                                'valueformat':',g',
                                'relative':False,
                                'font':{'size':15}},
                        number={'valueformat':',',
                                'font':{'size':20}},
                        domain={'y':[0, 1], 'x': [0, 1]}
    )]
    layout = go.Layout(title={'text':'GSV (bbls)',
                                'y':1,
                                'x':0.5,
                                'xanchor':'center',
                                'yanchor':'top'},
                        font=dict(color=color),
                        paper_bgcolor='#f3f3f3',
                        plot_bgcolor='#f3f3f3',
                        height=50)
    return {'data': indicator, 'layout':layout}
