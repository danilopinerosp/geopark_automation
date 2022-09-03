from dash import Input, Output, State, callback_context
import plotly.graph_objs as go
from dash import html

# Librerías para el tratamiento de datos
import numpy as np

from openpyxl import load_workbook
from pages.balance.balance_data import (
            agregar_estilos, 
            calculate_inventory_oil_type, 
            calculate_total_inventory,
            generate_report_ODCA, 
            get_cumulated,
            remove_entries_balance, 
            total_oil_detailed)
from openpyxl.utils import get_column_letter
import datetime

from components.indicator import graph_indicator

from app import app

from pages.balance.balance_data import (get_cumulated, 
                                        update_indicators,
                                        read_data_daily_reports,
                                        clean_balance_data,
                                        oil_sender_operation,
                                        write_data_monthly_report)

from utils.functions import load_data, filter_data_by_date, log_processed, parse_contents, verify_processed, write_data
from utils.constants import balance_data, daily_reports_processed, months

inputs_cumulated = [Input('balance-period-analysis', 'start_date'),
            Input('balance-period-analysis', 'end_date'),
            Input('tipo-operacion', 'value')]

# Callback para actualizar el GOV acumulado para geopark
@app.callback(Output('GOV-acumulado-geopark', 'children'), inputs_cumulated)
def update_gov_cumulated_geopark(start_date, end_date, operation_type):
    """
    Actualiza el GOV acumulado para Geopark en el periodo indicado
    """
    data = load_data(balance_data)
    return get_cumulated(data, start_date, end_date, operation_type, 'GOV', 'GEOPARK')

# Callback para actualizar el GSV acumulado para geopark
@app.callback(Output('GSV-acumulado-geopark', 'children'), inputs_cumulated)
def update_gsv_cumulated_geopark(start_date, end_date, operation_type):
    """
    Actualiza el total de GSV producido por Geopark en periodo de tiempo indicado
    """
    data = load_data(balance_data)
    return get_cumulated(data, start_date, end_date, operation_type, 'GSV', 'GEOPARK')

# Callback para actualizar el NSV acumulado para Geopark
@app.callback(Output('NSV-acumulado-geopark', 'children'), inputs_cumulated)
def update_nsv_cumulated_geopark(start_date, end_date, operation_type):
    """
    Actualiza en acumulado de NSV producido por Geopark en el periodo de tiempo indicado
    """
    data = load_data(balance_data)
    return get_cumulated(data, start_date, end_date, operation_type, 'NSV', 'GEOPARK')

# Callback para actualizar el NSV acumulado para Parex
@app.callback(Output('GOV-acumulado-parex', 'children'), inputs_cumulated)
def update_gov_cumulated_parex(start_date, end_date, operation_type):
    """
    Actualiza el GOV acumulado en el periodo indicado para Parex
    """
    data = load_data(balance_data)
    return get_cumulated(data, start_date, end_date, operation_type, 'GOV', 'PAREX')

# Callback para actualizar el GSV acumulado para Parex
@app.callback(Output('GSV-acumulado-parex', 'children'), inputs_cumulated)
def update_gsv_cumulated_parex(start_date, end_date, operation_type):
    """
    Actualiza el GSV acumulado producido por Parex en el periodo de tiempo indicado
    """
    data = load_data(balance_data)
    return get_cumulated(data, start_date, end_date, operation_type, 'GSV', 'PAREX')

# Callback para actualizar el NSV acumulado para Parex
@app.callback(Output('NSV-acumulado-parex', 'children'), inputs_cumulated)
def update_nsv_cumulated_parex(start_date, end_date, operation_type):
    """
    Actualiza el total de NSV acumulado para Parex en el periodo de tiempo indicado
    """
    data = load_data(balance_data)
    return get_cumulated(data, start_date, end_date, operation_type, 'NSV', 'PAREX')

# Callback for uploading reports
@app.callback(Output("files-to-process", "children"),
            [Input("subir-reporte-diario", 'contents')],
            [State('subir-reporte-diario', 'filename'),
            State('subir-reporte-diario', 'last_modified')])
def update_daily_reports(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = list()
        # Nombres de los valores a guardar en el balance
        header = ['fecha', 'empresa', 'operacion', 'tipo crudo', 'GOV', 'GSV', 'NSV']
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            try:
                book = parse_contents(c, n, d)
                list_data = read_data_daily_reports(book, n, 1, 270)
                if verify_processed(n, daily_reports_processed):
                    new_data = remove_entries_balance(balance_data, n)
                    new_data.to_csv(balance_data, index=False)
                else:
                    log_processed(n, daily_reports_processed, ["fecha actualizacion", "fecha reporte"], "reporte")
                data_cleaned = clean_balance_data(list_data)
                write_data(balance_data, header, data_cleaned)

                children.append(html.P(n))
            except Exception as e:
                children.append(html.Div(['There was an error processing this file.']))

        return children

# Callback for downloading button
@app.callback(Output("downloaded-report", "children"),
            [Input("descargar-acta", "n_clicks"),
            Input('balance-period-analysis', 'start_date'),
            Input('balance-period-analysis', 'end_date')],
)
def download_balance_report(n_clicks, start_date, end_date):
    # Cargar los datos desde el balance y dar formato a las fechas
    data = load_data(balance_data)
    filtered_data = filter_data_by_date(data, start_date, end_date)
    try:
        month = filtered_data['fecha'].dt.month.unique()[0]
        year = filtered_data['fecha'].dt.year.unique()[0]
    except:
        month = 0
        year = 0
    return generate_report_ODCA(data, month, year)

# Callback para actualizar la producción del último día reportado de GOV
# para Geopark
@app.callback(Output('GOV-geopark', 'figure'),
            [Input('tipo-operacion', 'value')])
def update_gov_geopark(operation_type):
    """
    Actualiza los datos de GOV de la producción del último día reportado
    para Geopark
    """
    data = load_data(balance_data)
    (last_gov, previous_gov) = update_indicators(data, operation_type, "GOV")
    return graph_indicator(last_gov, previous_gov, "orange", "GOV")
    
# Callback para actualizar los datos de producción de GSV de Geopark en el último día reportado
@app.callback(Output('GSV-geopark', 'figure'),
            [Input('tipo-operacion', 'value')])
def update_gsv_geopark(operation_type):
    """
    Actualiza la producción de GSV producida por Geopark en el último día reportado
    de producción
    """
    data = load_data(balance_data)
    (last_gsv, previous_gsv) = update_indicators(data, operation_type, "GSV")
    return graph_indicator(last_gsv, previous_gsv, "#dd1e35", "GSV")

# Callback para actualizar los datos de producción de NSV de Geopark en el último día reportado
@app.callback(Output('NSV-geopark', 'figure'),
            [Input('tipo-operacion', 'value')])
def update_nsv_geopark(operation_type):
    """
    Actualiza el NSV producido por Geopark en el último día reportado de operación
    """
    data = load_data(balance_data)
    (last_nsv, previous_nsv) = update_indicators(data, operation_type, "GSV")
    return graph_indicator(last_nsv, previous_nsv, "green", "NSV")

# Render title for company participation in NSV production
@app.callback(Output("title-participation-company", "children"),
            Input('tipo-operacion', 'value'))
def update_title_participation_company(operation_type):
    title = f"Participación {operation_type.split()[0].capitalize()} NSV"
    return title

# Callback para actualizar la gráfica de participación de la empresa
@app.callback(Output('participation-company', component_property='figure'),
            [Input('balance-period-analysis', 'start_date'),
            Input('balance-period-analysis', 'end_date'),
            Input('tipo-operacion', 'value')]
)
def update_participation(start_date, end_date, value):
    """
    Actualizar el pie que contiene la participación de la empresa por tipo de operación
    en la producción de NSV
    """
    data = load_data(balance_data)
    filtered_data = filter_data_by_date(data, start_date, end_date)
    # datos_filtrados = datos_filtrados[datos_filtrados['operacion'] == value]
    colors = ['red', 'grey']
    # Calcular total de producción diaria para NSV para determinado tipo de operación por empresa
    filtered_data = oil_sender_operation(filtered_data, 'NSV', value)
    if filtered_data.shape != (0,0):
        labels = filtered_data.columns.values
        values = [round(np.sum(filtered_data[empresa]), 2) for empresa in filtered_data.columns]
    else:
        labels = ["Aún no hay datos"]
        values = [0]
    trace =[go.Pie(labels=labels,
                    values=values,
                    hoverinfo='percent',
                    textinfo='label+value',
                    textfont=dict(size=13),
                    hole=.5,
                    rotation=45,
                    textposition='outside',
                    marker=dict(colors=colors)
                )
            ]
    layout = go.Layout(
        plot_bgcolor='#f3f3f3',
            paper_bgcolor='#f3f3f3',
            hovermode='closest',
            legend={
                'orientation': 'h',
                'bgcolor': '#f3f3f3',
                'xanchor': 'center', 'x': 0.5, 'y': -0.15},
            font=dict(
                family="sans-serif",
                size=12,
                color='#262830'),
            margin=dict(t=60, b=30, l=30, r=30)
            )
    return {'data':trace, 'layout':layout}


# Callback to update title for historical nsv per company
@app.callback(Output("title-historical-nsv", "children"),
            [Input('balance-period-analysis', 'start_date'),
            Input('balance-period-analysis', 'end_date'),
            Input('tipo-operacion', 'value')])
def update_title_hystorical_nsv(start_date, end_date, operation_type):
    title = f"{ operation_type.split()[0].capitalize() } NSV (bbls)"
    return title

# Callback para actualizar la gráfida de los resultados históricos de la operación para cada empresa
@app.callback(Output('NSV-historico', component_property='figure'),
            [Input('balance-period-analysis', 'start_date'),
            Input('balance-period-analysis', 'end_date'),
            Input('tipo-operacion', 'value')]
)
def update_hystorical(start_date, end_date, value):
    """
    Actualiza la gráfica de los resultados históricos de la operación para cada empresa
    y para el periodo de tiempo indicado
    """
    data = load_data(balance_data)
    filtered_data = filter_data_by_date(data, start_date, end_date)
    colors = ['red', 'grey']
    traces = []

    if filtered_data.shape != (0,0):
        filtered_data = oil_sender_operation(filtered_data, 'NSV', value)
        for i, empresa, in enumerate(filtered_data.columns.values):
            traces.append(go.Scatter(x=filtered_data.index,
                                y=filtered_data[empresa],
                                name=empresa,
                                line={'width':4, 'color':colors[i]},
                                mode='lines+markers'))
    layout = go.Layout(plot_bgcolor='#f3f3f3',
            paper_bgcolor='#f3f3f3',
            hovermode='closest',
            legend={
                'orientation': 'h',
                'bgcolor': '#f3f3f3',
                'xanchor': 'center', 'x': 0.5, 'y': -0.15},
            font=dict(
                family="sans-serif",
                size=12,
                color='#262830'),
            margin=dict(t=60, b=30, l=30, r=30)
            )
    return {'data': traces, 'layout': layout}

# Callback to update title for cummulated nsv per oil type
@app.callback(Output("title-cumulated", "children"),
            [Input('tipo-operacion', 'value'),
            Input('condiciones-operacion', 'value')])
def update_title_cummulated_nsv(operation_type, operation_conditions):
    title = f"{ operation_type.split()[0].capitalize() } de { operation_conditions } por tipo de crudo (bbls)"
    return title

# Callback para actualizar la gráfica de barras sobre la producción por campo
# para determinado tipo de crudo
@app.callback(Output('graph-cumulated', component_property='figure'),
            [Input('balance-period-analysis', 'start_date'),
            Input('balance-period-analysis', 'end_date'),
            Input('tipo-operacion', 'value'),
            Input('condiciones-operacion', 'value')]
)
def update_company_results(start_date, end_date, operation_type, oil_condition):
    """
    Actualiza la gráfica de barras sobre la producción por campo para determinado tipo de crudo
    """
    data = load_data(balance_data)
    # Filtrar los datos para el período indicado, el tipo de operación de interés y el tipo de crudo
    filtered_data = filter_data_by_date(data, start_date, end_date)
    traces = []
    colors = ['red', 'grey']
    if filtered_data.shape != (0,0):
        filtered_data = total_oil_detailed(filtered_data, operation_type)[oil_condition]
        for i, company in enumerate(filtered_data.index):
            traces.append(go.Bar(name=company,
                        x=filtered_data.columns.values,
                        y=filtered_data.loc[company, :],
                        marker={'color': colors[i]},
                        text=filtered_data.loc[company, :].round(2),
                        textposition='outside'))

    layout = go.Layout(font=dict(color='#262830'),
                        paper_bgcolor='#f3f3f3',
                        plot_bgcolor='#f3f3f3',
                        barmode='group',
                        margin=dict(t=60, b=60, l=30, r=30), 
                        )
    return {'data':traces, 'layout':layout}

# Callback to update company inventory graph
@app.callback(Output("title-inventory", "children"),
            [Input('condiciones-operacion', 'value'),
            Input("empresa", "value")]
)
def update_title_inventory(operation_conditions, company):
    title = f" Inventario { operation_conditions } { company } por tipo de crudo (bbls)"
    return title

# Callback para actualizar la gráfica de barras sobre el inventario por campo
# para determinado tipo de crudo
@app.callback(Output('inventario-empresa', component_property='figure'),
            [Input('balance-period-analysis', 'start_date'),
            Input('balance-period-analysis', 'end_date'),
            Input('empresa', 'value'),
            Input('condiciones-operacion', 'value')])
def update_inventory(start_date, end_date, company, tipo_crudo):
    """
    Actualiza la gráfica del inventario por empresa y por tipo de crudo
    """
    data = load_data(balance_data)
    filtered_data = filter_data_by_date(data, start_date, end_date)
    trace = []
    if filtered_data.shape != (0,0):
        inventario_campo = calculate_inventory_oil_type(filtered_data, company, tipo_crudo)
        trace = [go.Bar(name=company,
                        x=inventario_campo.index,
                        y=inventario_campo.values,
                        text=inventario_campo.values.round(2),
                        textposition='auto')]

    layout = go.Layout(font=dict(color='#262830'),
                        paper_bgcolor='#f3f3f3',
                        plot_bgcolor='#f3f3f3',
                        )
    return {'data':trace, 'layout':layout}

# Callback para mostrar el inventario total para determinado periodo, empresa y tipo de crudo
@app.callback(Output('inventario-total', component_property='children'),
            [Input('balance-period-analysis', 'start_date'),
            Input('balance-period-analysis', 'end_date'),
            Input('empresa', 'value'),
            Input('condiciones-operacion', 'value')])
def update_total_inventory(start_date, end_date, company, operation_condition):
    """
    Actualiza el inventario total por empresa y tipo de crudo para el
    periodo de tiempo indicado
    """
    data = load_data(balance_data)
    filtered_data = filter_data_by_date(data, start_date, end_date)
    total_inventory = 0
    if filtered_data.shape != (0,0):
        inventory_oil_type = calculate_inventory_oil_type(filtered_data, company, operation_condition)
        total_inventory = calculate_total_inventory(inventory_oil_type)
    return f'Inventario Total: {round(total_inventory, 2)}'
