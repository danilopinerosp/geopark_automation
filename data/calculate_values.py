"""
En este módulo se encuentran todas las funciones necesarias que
ayudan en la generación de todos los valores calculados para la
operación
"""

# Importar librerías para el tratamiendo de datos
import pandas as pd
import numpy as np

def leer_datos(documento):
    """
    Retorna un dataframe con los datos obtenidos a partir de documento

    Parámetros:
    -----------
    documento -> str - Cadena de caracteres con la ruta al documento .csv que contiene
                        los datos a cargar

    Retorna:
    --------
    df -> DataFrame - Contiene los datos cargados de documento
    """
    datos = pd.read_csv(documento)
    return datos

def total_crudo_detallado(datos, tipo_operacion):
    """
    Retorna un DataFrame con el total de Crudo según las condiciones de operación,
    el campo y el remitente.

    Parámetros:
    -----------
    datos -> DataFrame - Contiene los datos de crudo por tiempo de operación, campo y empresa.

    Retorna:
    --------
    total_crudo -> DataFrame - Totales por condiciones de operación, campo y remitente
    """
    # Filtrar los datos por tipo de operación
    total_crudo = datos[[tipo_operacion in fila for fila in datos['operacion']]]
    # Calcular los totales por condiciones de operación, campo y empresa
    total_crudo =  total_crudo.groupby(['empresa', 'campo'])[['GOV', 'GSV', 'NSV']].sum().unstack()
    # Se retorna el DataFrame con los totales, no sin antes remplazar los NaN por ceros.
    return total_crudo.fillna(0)

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

def filtrar_datos_fechas(datos, inicio, fin):
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
    datos = datos[(datos['fecha'] >= inicio) & (datos['fecha'] <= fin)]
    datos['fecha'] = pd.to_datetime(datos['fecha'])
    return datos

def calcular_diferencias(datos, operacion_1, operacion_2, tipo_crudo='NSV', empresa='GEOPARK'):
    """
    Retorna un DataFrame con el resultado de restar los datos de la caterogia_2 a la
    categoria_1 para cada día de operación por empresa y campo

    Parámetros:
    -----------
    datos  -> DataFrame - datos del balance
    categoria_1 -> str - cadena de caracteres con la primera categoría de donde vamos
                        a hacer la resta
    categoria_2 -> str - cadena de caracteres con al segunda categoría que le vamos
                        a restar a la primera categoría
    tipo_crudo -> str - Indica el tipo de crudo al cual se le van a sacar las diferentes
                        entre las dos categorías
    """
    # Filtrar los datos según las dos categorías a analizar
    filtro = (datos['operacion'] ==  operacion_1) | (datos['operacion'] == operacion_2)
    datos_filtrados = datos[filtro]
    # Agrupar los datos para realizar las respectivas diferencias
    agrupados = datos_filtrados.groupby(['fecha', 'campo', 'empresa', 'operacion'])[tipo_crudo]
    # Separar los datos agrupados por operación
    op_1 = agrupados.sum().unstack().unstack().fillna(0)[operacion_1]
    op_2 = agrupados.sum().unstack().unstack().fillna(0)[operacion_2]
    # Calcular las diferencias
    diferencias = (op_1 - op_2).unstack().fillna(0)
    return diferencias[empresa]

def calcular_inventario_campo(datos, empresa, tipo_crudo, inventario_inicial_campo=None):
    """
    Retorna el inventario final por campo al sumar y restar las diferencias dadas
    en inventario_diario_campo del inventario_inicial_campo

    Parámetros:
    -----------
    Datos -> DataFrame - Contiene los datos de la operación diaria de las empresas
    empresa -> str - Nombre de la empresa a la que le calculamos el inventario
    tipo_crudo -> str - Cadena de caracteres con el tipo de crudo a analizar
    inventario_inicial_campo -> dict - Diccionario con el inventario inicial para cada campo

    Retorna:
    --------
    pandas.core.series.Series -> Inventario por campo para la empresa indicada.
    """
    # calcular las diferencias para la empresa para determinado tipo de crudo
    diferencias = calcular_diferencias(datos,
                                        'RECIBO POR REMITENTE TIGANA',
                                        'DESPACHO POR REMITENTE',
                                        tipo_crudo, empresa)
    # Agregar el inventario inicial por campo al dataframe de las diferencias
    if inventario_inicial_campo is not None:
        diferencias = pd.concat([diferencias, pd.Series(inventario_inicial_campo, dtype='float64')])
    # Eliminar las columnas que continen los datos de TIGANA y JACANA
    diferencias.drop(['JACANA ESTACION', 'TIGANA ESTACION'], inplace=True, axis=1)
    # Retornar el inventario final de los datos
    return np.round(diferencias.sum(), 2)

def calcular_inventario_total(inventario_campo):
    """
    Retorna la suma del inventario por campo.

    Parámetros:
    -----------
    pandas.core.series.Series - inventario por campo

    Retorna:
    float - Suma total de cada inventario por campo
    """
    return inventario_campo.sum()

if __name__ == "__main__":
    from datetime import datetime as dt
    from datetime import timedelta
    inicio = dt.today() - timedelta(10)
    fin = inicio + timedelta(3)
    datos = pd.read_csv('datos/balance.csv')
    datos['fecha'] = pd.to_datetime(datos['fecha'], format='%d-%m-%Y')
    print(calcular_inventario_total(calcular_inventario_campo(datos, 'GEOPARK', 'NSV')))
