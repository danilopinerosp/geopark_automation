"""
En este módulo se encuentran todas las funciones necesarias que
ayudan en la generación de todos los valores calculados para la
operación
"""

# Importar librerías para el tratamiendo de datos
import pandas as pd
import numpy as np

def total_crudo_empresa(datos, tipo_operacion):
    """
    Retorna un DataFrame con el total de crudo por tipo de operación y empresa.

    Parámetros:
    ----------
    datos -> DataFrame - Contiene los datos de la operación

    Retorna:
    --------
    retultado -> DataFrame - Contiene los totales calculados por condiciones
                            de operación y por empresa.
    """
    # Filtrar los datos por tipo de operación
    total_crudo = datos[[tipo_operacion in fila for fila in datos['operacion']]]
    # Calcular los totales por condiciones de operación y empresa
    total_crudo =  total_crudo.groupby(['empresa'])[['GOV', 'GSV', 'NSV']].sum()
    # Se retorna el DataFrame con los totales, no sin antes remplazar los NaN por ceros.
    return total_crudo.fillna(0)

def total_crudo(datos, tipo_operacion):
    """
    Retorna el total acumulado por condiciones de operación.

    Parámetros:
    -----------
    datos -> DataFrame - contiene los datos en bruto de la operación
    tipo_operacion -> str - tipo de operación a la que le queremos calcular los totales.
                            Puede tener los valores "RECIBO", "DESPACHO", "ENTREGA".

    Retorna:
    -------
    resultado -> panda.Series - Una serie que contiene los totales por condiciones
                                de operación del crudo.
    """
    resultado = total_crudo_empresa(datos, tipo_operacion).sum()
    return resultado

def total_nsv_recibo(datos):
    """
    Retorna un diccionario con el valor total de NSV recibido por remitente y en general.

    Parámetros:
    ----------
    datos -> DataFrame - Datos ya filtrados del NSV recibido diario por cada remitente.

    Retorna:
    --------
    total_nsv -> dict - Diccionario con los totales de NSV recibido y el total en general.
    """
    total_nsv = dict() # Diccionario para almacenar los totales
    empresas = datos.columns  # Extraer las empresas
    total = 0
    for empresa in empresas:
        total_nsv[empresa] = datos[empresa].sum() # Calcular el total por empresa
        total += total_nsv[empresa] # Acumular el total de cada empresa
    total_nsv['TOTAL'] = total # Agregar al diccionario el total de NSV
    return total_nsv

if __name__ == "__main__":
    from datetime import datetime as dt
    from datetime import timedelta
    inicio = dt.today() - timedelta(10)
    fin = inicio + timedelta(3)
    datos = pd.read_csv('datos/balance.csv')
    datos['fecha'] = pd.to_datetime(datos['fecha'], format='%d-%m-%Y')
