def leer_datos(documento):
    """
    Retorna un dataframe con los datos obtenidos a partir de documento

    Parámetros:
    -----------
    documento -> str - Cadena de caracteres con la ruta al documento .csv que contiene los datos a cargar

    Retorna:
    --------
    df        -> DataFrame - Contiene los datos cargados de documento
    """
    import pandas as pd
    df = pd.read_csv(documento)
    return df

def nsv_recibo_remitente(datos):
    """
    Retorna un DataFrame con el total de NSV recibido diario por cada remitente.

    Parámetros:
    -----------
    datos -> DataFrame - Contiene los datos del balance que serán usados para calcular el todal de NSV recibido diario por cada empresa.

    Retorna:
    -------
    -> DataFrame - DataFrame que contiene el total diario de NSV por cada empresa, una columna contiene los resultados de una empresa.
    """
    # Filtrar solo los datos cuya operación es un recibo
    recibidos = datos[['RECIBO' in fila for fila in datos['operacion']]]
    return recibidos.groupby(['fecha', 'empresa'])['NSV'].sum().unstack()

def total_crudo_detallado(datos, tipo_operacion):
    """
    Retorna un DataFrame con el total de Crudo según las condiciones de operación, el campo y el remitente.

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
    retultado -> DataFrame - Contiene los totales calculados por condiciones de operación y por empresa.
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
    resultado -> panda.Series - Una serie que contiene los totales por condiciones de operación del crudo.
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

def nsv_despacho_remitente(datos):
    """
    Retorna un DataFrame con el total de NSV daspachado diariamente por cada remitente.

    Parámetros:
    -----------
    datos -> DataFrame - Contiene los datos del balance que serán usados para calcular el todal de NSV despachado diario por cada empresa.

    Retorna:
    -------
    -> DataFrame - DataFrame que contiene el total diario de NSV por cada empresa, una columna contiene los resultados de una empresa.
    """
    # Filtrar unicamente los datos cuya operación es un despacho
    despachos = datos[['DESPACHO' in fila for fila in datos['operacion']]]
    # Filtrar los datos que no contienen Tigana y Jacana
    despachos = despachos[(despachos['campo'] != 'TIGANA ESTACION') & (despachos['campo'] != 'JACANA ESTACION')]
    # Calcular despachos de NSV diario por empresa
    despachos = despachos.groupby(['fecha', 'empresa'])['NSV'].sum().unstack()
    # Se retorna el DataFrame con los datos calculados, y se remplazan los valores NaN por 0.
    return despachos.fillna(0)

def filtrar_datos_fechas(datos, inicio, fin):
    """
    Retorna un DataFrame en el cual se contienen únicamente los datos que se encuentran entre las fechas inicio
    y fin recibidas como parámetro.

    Parámetros:
    -----------
    datos -> DataFrame - Contiene los datos a filtrar por fechas
    inicio -> datetime - Fecha de inicio del período en el formado '%d-%m-%Y'
    fin    -> datetime - Fecha de fin del período en el formato '%d-%m-%Y'

    Retorna:
    DataFrame - Datos filtrados según el período dato entre inicio y fin
    """
    return datos[(datos['fecha'] >= inicio) & (datos['fecha'] <= fin)]

def diferencias(datos, categoria_1, cateroria_2):
    """
    Retorna un DataFrame con el resultado de restar los datos de la caterogia_2 a la categoria_1

    Parámetros:
    -----------
    datos  -> DataFrame - datos del balance
    categoria_1 -> str - cadena de caracteres con la primera categoría de donde vamos a hacer la resta
    categoria_2 -> str - cadena de caracteres con al segunda categoría que le vamos a restar a la primera categoría
    """
    pass

if __name__ == "__main__":
    from datetime import datetime as dt
    from datetime import timedelta
    import pandas as pd
    inicio = dt.today() - timedelta(10)
    fin = inicio + timedelta(3)
    datos = pd.read_csv('balance.csv')
    datos['fecha'] = pd.to_datetime(datos['fecha'], format='%d-%m-%Y')
    print(filtrar_datos_fechas(datos, inicio, fin))
