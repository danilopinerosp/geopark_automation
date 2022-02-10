import os

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
            writer = csv.DictWriter(documento_csv, fieldnames=head)
            writer.writerows(datos)
    else:
        with open(nombre_documento, 'w') as documento_csv:
            # Si el documento no existe se abre en modo escritura
            writer = csv.DictWriter(documento_csv, fieldnames=cabecera)
            writer.writeheader() # escribir la cabecera
            writer.writerows(datos)
