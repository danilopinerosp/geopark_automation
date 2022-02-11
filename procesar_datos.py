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

if __name__ == "__main__":
    datos = leer_datos('balance.csv')
    print(nsv_despacho_remitente(datos))