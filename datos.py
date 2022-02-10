# Declaración de constantes
EMPRESAS = ['GEOPARK', 'PAREX']
CAMPOS = ['CHIRICOCA', 'INDICO-2', 'INDICO-1X', 'AZOGUE', 'GUACO', 'ADALIA',
            'AKIRA', 'MARACAS', 'CARMENTEA', 'CALONA', 'CAPACHOS', 'JACANA ESTACION',
            'TIGANA ESTACION']
OPERACIONES = ['DESPACHO POR REMITENTE', 'RECIBO POR REMITENTE JACANA',
                'RECIBO POR REMITENTE TIGANA', 'ENTREGA POR REMITENTE']

def escribir_datos(nombre_documento, cabecera, datos):
    """
    Crea un documento .csv con el nombre_documento indicado en el parámetro que recibe.

    Parámetros:
    ----------
    nombre_documento -> str - Cadena de caracteres con el nombre del documento a crear
    cabecera   -> str - Cadena de caracteres con los nombres de las columnas
    datos  -> dict - Diccionario con los datos a almacenar en el documento
    """
    # Cargar librerias necesarias para crear el documento de los datos del documento
    import csv
    import os
    # Verificar si el documento existe
    if os.path.exists(nombre_documento):
        # Si nombre_documento existe se abre en modo append ('agregar informacion')
        with open(nombre_documento, 'a') as documento_csv:
            writer = csv.DictWriter(documento_csv, fieldnames=cabecera)
            writer.writerows(datos)
    else:
        with open(nombre_documento, 'w') as documento_csv:
            # Si el documento no existe se abre en modo escritura
            writer = csv.DictWriter(documento_csv, fieldnames=cabecera)
            writer.writeheader() # escribir la cabecera
            writer.writerows(datos)

def leer_datos(documento, inicio, fin):
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
    # Cargar las librerías necesaria para leer el }
    import openpyxl

    #Cargar el documento excel
    book = openpyxl.load_workbook(documento)
    sheet =  book.active #Por defecto toma como activa la primera hoja

    #Extraer le fecha del reporte del nombre del documento
    fecha = documento.split('Reportes')[-1].split()[2].split('.')[0]

    lista_datos = list() # Para almacenar la lista de diccionarios

    # Recorrer todas las filas del documento excel y extraer los valores
    for i in range(inicio, fin):
        columna_b = 'B' + str(i) # ayuda a recorrer la columna B
        valor = sheet[columna_b].value
        datos = dict()     # Almacena los datos por cada entrada
        if valor in EMPRESAS:
            empresa = valor
            continue
        if valor in OPERACIONES:
            operacion = valor
            continue
        if valor in CAMPOS:
            # si valor se encuentra en la constante CAMPO guarda todos los leer_datos
            # en el diccionario datos
            datos['fecha'] = fecha
            datos['empresa'] = empresa
            datos['operacion'] = operacion
            datos['campo'] = valor
            datos['GOV'] = sheet['D' + str(i)].value
            datos['GSV'] = sheet['E' + str(i)].value
            datos['NSV'] = sheet['F' + str(i)].value
            lista_datos.append(datos) # agreagar los datos a la lista de datos
    return lista_datos

def limpiar_datos(datos):
    """
    La función es la encargada de limpiar los datos cuando estos no tienen el tipo de datos esperado,
    o tienen campo vacios que los hacen inválidos.

    Parámetros:
    -----------
    datos -> list - Lista de diccionarios con los datos a limpiar

    Retorna:
    --------

    """
    procesados = list()
    for dato in datos: 
        # Remover los diccionarios con GVO, GSV  NSV vacíos
        if not dato['GOV'] and not dato['GSV'] and not dato['NSV']:
            continue
        procesados.append(dato)
    return procesados
            


if __name__ == "__main__":
    import os
    cabecera = ['fecha', 'empresa', 'operacion', 'campo', 'GOV', 'GSV', 'NSV']
    reportes = os.path.abspath('..\Reportes')
    for reporte in os.listdir(reportes):
        ruta = os.path.join(reportes, reporte)
        datos = leer_datos(ruta, 1, 206)
        escribir_datos('balance.csv', cabecera, limpiar_datos(datos))