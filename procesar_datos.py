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
    recibidos = datos[['RECIBO' in fila for fila in datos['operacion']]]
    return recibidos.groupby(['fecha', 'empresa'])['NSV'].sum().unstack()   

if __name__ == "__main__":
    datos = leer_datos('balance.csv')
    print(nsv_recibo_remitente(datos))