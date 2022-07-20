from openpyxl import load_workbook
import pandas as pd
import io
import base64
import datetime
from dash import html

def load_data(filename):
    """
    Load the balance data from the balance.csv file
    """
    df = pd.read_csv(filename)
    df['fecha'] = pd.to_datetime(df['fecha'], format='%d-%m-%Y')
    return df

def filter_data_by_date(data, start_date, end_date):
    """
    Retorna un DataFrame en el cual se contienen únicamente los datos que se encuentran
    entre las fechas inicio y fin recibidas como parámetro.

    Parámetros:
    -----------
    datos -> DataFrame - Contiene los datos a filtrar por fechas
    inicio -> datetime - Fecha de inicio del período en el formado '%d-%m-%Y'
    fin    -> datetime - Fecha de fin del período en el formato '%d-%m-%Y'

    Retorna:
    DataFrame - Datos filtrados según el período dato entre inicio y fin
    """
    filtered_data = data[(data['fecha'] >= start_date) & (data['fecha'] <= end_date)]
    # filtered_data['fecha'] = pd.to_datetime(filtered_data['fecha'])
    return filtered_data

def parse_contents(contents, filename, date):
    """
    Return workbook
    """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    if 'xls' in filename:
        # Assume that the user uploaded an excel file
        return load_workbook(io.BytesIO(decoded))
    else:
        return "Wrong format, file should have .xlsx extension"
