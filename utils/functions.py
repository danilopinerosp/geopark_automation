from openpyxl import load_workbook
import pandas as pd
import io
import base64
import datetime
from dash import html
import os
import csv

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
    try:
        filtered_data = data[(data['fecha'] >= start_date) & (data['fecha'] <= end_date)]
    except:
        filtered_data = pd.DataFrame()
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
        return load_workbook(io.BytesIO(decoded), data_only=True)
    return -1

def write_data(filename, header, data):
    """
    Crea un documento .csv con el nombre_documento indicado en el parámetro que recibe.

    Parámetros:
    ----------
    nombre_documento -> str - Cadena de caracteres con el nombre del documento a crear
    cabecera   -> str - Cadena de caracteres con los nombres de las columnas
    datos  -> dict - Diccionario con los datos a almacenar en el documento
    """
    # Verificar si el documento existe
    if os.path.exists(filename):
        # Si nombre_documento existe se abre en modo append ('agregar informacion')
        with open(filename, 'a',  newline='') as csv_document:
            writer = csv.DictWriter(csv_document, fieldnames=header)
            writer.writerows(data)
    else:
        with open(filename, 'w', newline='') as csv_document:
            # Si el documento no existe se abre en modo escritura
            writer = csv.DictWriter(csv_document, fieldnames=header)
            writer.writeheader() # escribir la cabecera
            writer.writerows(data)

def log_processed(report, filepath, header, type_processed):
    """
    Agregar el reporte al documento de reportes procesados, en caso de que el documento
    no exista, lo creará y luego agregará el reporte. El documento reportes_procesados
    continene la fecha en la que se procesó el reporte y el nombre del reporte procesado.

    Parámetros:
    -----------
    reporte -> str - Cadena de caracteres con el nombre del reporte procesado
    """
    data = [{'fecha actualizacion': datetime.date.today(), f'fecha {type_processed}': report}]
    write_data(filepath, header, data)

def verify_processed(report, filepath):
    """
    Retorna verdadero si encuentra el reporte en el documento reportes procesados,
    retorna false si el documento no existe o si no ha encontrado el reporte en él.

    Parámetros:
    -----------
    reporte -> str - Cadena de caracteres con el nombre del reporte a verificar

    Retorna:
    --------
    found -> bool - Verdadero si encontró el reporte, falso en otro caso
    """
    found = False
    if os.path.exists(filepath):
        with open(filepath, 'r') as reports:
            reader = csv.DictReader(reports)
            for processed in reader:
                if processed['fecha reporte'] == report:
                    found = True
    return found
    