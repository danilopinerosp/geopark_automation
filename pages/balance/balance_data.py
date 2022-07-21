import numpy as np

from utils.functions import filter_data_by_date

from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import datetime
import pandas as pd

import os
import csv

EMPRESAS = ['GEOPARK', 'PAREX']
CAMPOS = ['CHIRICOCA', 'INDICO-2', 'INDICO-1X', 'AZOGUE', 'GUACO', 'ADALIA',
            'AKIRA', 'MARACAS', 'CARMENTEA', 'CALONA', 'CAPACHOS', 'JACANA ESTACION',
            'TIGANA ESTACION', 'CABRESTERO - BACANO JACANA ESTACION']
OPERACIONES = ['DESPACHO POR REMITENTE', 'RECIBO POR REMITENTE JACANA',
                'RECIBO POR REMITENTE TIGANA', 'ENTREGA POR REMITENTE']
CONDICIONES = ['GOV', 'GSV', 'NSV']

def get_date_last_report(data):
    try:
        return data['fecha'].max().strftime('%d/%m/%Y')
    except:
        return "Aún no hay datos"

def get_cumulated(data, start_date, end_date, operation_type, operation_condition, company):
    filtered_data = filter_data_by_date(data, start_date, end_date)
    if filtered_data != 0:
        filtered_data = filtered_data[['empresa', 'operacion', operation_condition]]
        filter = (filtered_data['operacion'] == operation_type) & (filtered_data['empresa'] == company)
        cumulated = filtered_data[filter][operation_condition].sum()
    else:
        cumulated = filtered_data
    return f"{cumulated:,.2f}"

def update_indicators(data, operation_type, operation_conditions):
    try:
        # Agrupar los valores del DataFrame y hacer una suma por cada grupo
        datos_agrupados = data.groupby(['fecha', 'empresa', 'operacion'])[operation_conditions].sum()
        # Seleccionar el GOV para el último día reportado
        last = np.round(datos_agrupados.unstack().unstack()[operation_type]['GEOPARK'][-1], 2)
        # Seleccionar el GOV para el penúltimo día reportado
        previous = np.round(datos_agrupados.unstack().unstack()[operation_type]['GEOPARK'][-2], 2)
    except:
        last = 0
        previous = 0
    return (last, previous)

def read_data_daily_reports(book, filename, start_cell=1, end_cell=270):
    """
    Leer los datos del documento que recibe como parámetro y retorna una
    lista de diccionarios con todos los datos de documento

    Parámetros:
    -----------
    documento -> str - Cadena de caracteres que contiene la ruta del
                        documento de donde se quieren leer los leer_datos
    Return:
    ------
    list -> Retorna una lista de diccionarios con los datos del documento.
    """
    sheet =  book.active #Por defecto toma como activa la primera hoja

    #Extraer le fecha del reporte del nombre del documento
    file_date = filename.split('Reportes')[-1].split()[2].split('.')[0]

    list_data = list() # Para almacenar la lista de diccionarios

    # Recorrer todas las filas del documento excel y extraer los valores
    for i in range(start_cell, end_cell):
        column_b = 'B' + str(i) # ayuda a recorrer la columna B
        value_cell = sheet[column_b].value
        datos = dict()     # Almacena los datos por cada entrada
        if value_cell in EMPRESAS:
            company = value_cell
            continue
        if value_cell in OPERACIONES:
            operation = value_cell
            continue
        if value_cell in CAMPOS:
            # si valor se encuentra en la constante CAMPO guarda todos los datos
            # en el diccionario datos
            datos['fecha'] = file_date
            datos['empresa'] = company
            datos['operacion'] = operation
            datos['campo'] = value_cell
            datos['GOV'] = sheet['D' + str(i)].value
            datos['GSV'] = sheet['E' + str(i)].value
            datos['NSV'] = sheet['F' + str(i)].value
            list_data.append(datos) # agreagar los datos a la lista de datos
    return list_data

def clean_balance_data(data):
    """
    La función es la encargada de limpiar los datos cuando estos no tienen el
    tipo de datos esperado, o tienen campo vacios que los hacen inválidos.

    Parámetros:
    -----------
    datos -> list - Lista de diccionarios con los datos a limpiar

    Retorna:
    --------

    """
    processed = list()
    for d in data:
        # Remover los diccionarios con GVO, GSV  NSV vacíos
        float_gov = isinstance(d['GOV'], float)
        float_gsv = isinstance(d['GSV'], float)
        float_nsv = isinstance(d['NSV'], float)
        if not float_gov and not float_gsv and not float_nsv:
            continue
        processed.append(d)
    return processed

def oil_sender_operation(data, operation_conditions, operation_type):
    """
    Retorna un DataFrame con el total por tipo de crudo de determinado operación diario
    por cada remitente.

    Parámetros:
    -----------
    datos -> DataFrame - Contiene los datos del balance que serán usados para calcular
                        el todal de NSV recibido diario por cada empresa.

    Retorna:
    -------
    -> DataFrame - DataFrame que contiene el total diario de NSV por cada empresa,
                    una columna contiene los resultados de una empresa.
    """
    try:
        # Filtrar solo los datos cuya operación es un recibo
        recibidos = data[[operation_type in fila for fila in data['operacion']]]
        result = recibidos.groupby(['fecha', 'empresa'])[operation_conditions].sum().unstack()
    except:
        result = 0
    return result

# Definición de funciones
def acumulado_mensual_campo(datos, mes, operacion, empresa):
    """
    Retorna un DataFrame con el acumulado por campo para cada tipo de crudo
    en el mes, tipo de operación y empresa indicados
    """
    datos_mes = datos[datos['fecha'].dt.month == mes]
    datos_operacion = datos_mes[datos_mes['operacion'] == operacion]
    datos_empresa = datos_operacion[datos_operacion['empresa'] == empresa]
    acumulado_mensual = datos_empresa.groupby('campo')[['GOV', 'GSV', 'NSV']].sum()
    # Retornas los acumulados mensuales redondeados a 2 decimales
    return acumulado_mensual.round(2).reset_index()

def estilo_celda(celda, background_color, font_color):
    """
    Agrega estilo a la celda indicada, y usa como background el color
    que recibe como parámetro
    """
    celda.fill = PatternFill('solid', fgColor=background_color)
    celda.alignment = Alignment(horizontal="center", vertical="center")
    thin = Side(border_style="thin", color="00000000")
    celda.border = Border(top=thin, left=thin, right=thin, bottom=thin)
    celda.font = Font(color=font_color, bold=True)

def agregar_estilos(hoja, filas, columna, background_color, font_color, header=True):
    """
    La función recibe una hoja de cálculo y se encarga de generar el estilo de la misma,
    agregando color a las celdas indicadas por las filas y la columna.
    """
    for fila in filas:
        celda = hoja.cell(row=fila, column=columna)
        # Dar estilo a la celda
        estilo_celda(celda, background_color, font_color)

        # Verificar si se trata de una cabecera
        if header:
            # Generar estilos para las celdas cuando se trata de una 
            # cabecera
            hoja.merge_cells(start_row=fila, start_column=columna, end_row=fila, end_column=columna + 3)
            # Estilo para las celdas restantes que no están en el merge
            for i in range(columna + 3, columna + 11):
                celda = hoja.cell(row=fila, column=i)
                estilo_celda(celda, background_color, font_color)
        else:
            # Agregar estilos para cuando se trata de celdas que no son parte
            # de la cabecera
            hoja.merge_cells(start_row=fila, start_column=columna, end_row=fila, end_column=columna + 10)

def write_data_monthly_report(data, month):
    """
    Escribir los datos acumulados por empresa y por tipo de operación en el
    ACTA para el mes indicado en un documento .xlsx
    """
    # Generar constante que almacena lo valores para la cabecera
    header = ['CAMPO','GOV (bls)','GSV (bls)','NSV (bls)','API @60ºF','S&W/Lab',
                '% Azufre','VISC 30 °C. /cSt']
    # Generar constante para cambiar los nombre de algunos valores
    names = {'RECIBO POR REMITENTE TIGANA': 'RECIBO POR REMITENTE EN TANQUE TK-780A',
                'PAREX': 'VERANO',
                'DESPACHO POR REMITENTE': 'DESPACHO POR REMITENTE',
                'ENTREGA POR REMITENTE': 'ENTREGA POR REMITENTE',
                'GEOPARK': 'GEOPARK'}
    # Declarar el objeto workbook
    book = Workbook()
    # Trabajar con la hoja activa.
    hoja = book.active
    hoja.insert_rows(1, amount=7)
    rows = 8
    filas_empresas = []
    filas_operaciones = []
    filas_cabecera = []
    try:
        for operation in data['operacion'].unique():
            hoja.append({6: names[operation]})
            rows += 1
            filas_operaciones.append(rows)
            for empresa in data['empresa'].unique():
                hoja.append({6: names[empresa]})
                rows += 1
                filas_empresas.append(rows)
                hoja.append({c + 6: value for c, value in enumerate(header)})
                rows += 1
                filas_cabecera.append(rows)
                acumulado = acumulado_mensual_campo(data, month, operation, 'GEOPARK')
                acumulado['campo'] = [f'ACUMULADO MENSUAL {campo}' for campo in acumulado['campo']]
                for r in dataframe_to_rows(acumulado, index=False, header=False):
                    hoja.append({c + 6: value for c, value in enumerate(r)})
                    rows += 1
                hoja.append(())
                rows += 1
    except Exception as e:
        print(e)
    hoja.insert_cols(7, amount=3)
    book.save("ACTA ODCA_" + str(month) + '.xlsx')
    return filas_cabecera, filas_empresas, filas_operaciones

def generar_acta_ODCA(mes):
    """
    Generar el acta con todos los datos requeridos y el estilo requerido
    """
    # Cargar los datos desde el balance y dar formato a las fechas
    df = pd.read_csv('data/consolidated_data/balance.csv')
    df['fecha'] = pd.to_datetime(df['fecha'], format='%d-%m-%Y')
    # Escribir los datos en un documento .xlsx
    filas_cabecera, filas_empresas, filas_operaciones = write_data_monthly_report(df, mes)
    # Cargar el documento generado anteriormente y seleccionar la hoja activa
    wb = load_workbook('ACTA ODCA_' + str(mes) + '.xlsx')
    ws = wb.active
    # Agregar estilos al acta
    agregar_estilos(ws, filas_cabecera, 6, "000000", "FFFFFF")
    agregar_estilos(ws, filas_operaciones, 6, "FF0000", "FFFFFF", False)
    agregar_estilos(ws, filas_empresas, 6,"FFFFFF", "000000", False)
    # Cambiar el ancho de las columnas de los datos
    for i in range(10, 17):
        letter = get_column_letter(i)
        ws.column_dimensions[letter].width = 15
    wb.save('ACTA ODCA_' + str(mes) +'.xlsx')