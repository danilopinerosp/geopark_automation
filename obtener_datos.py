"""
El modulo permite la optención de los datos a partir de los reportes diarios
de la operación que son entregados en formato .xlsx.
"""
# Cargar librerias necesarias para crear el documento de los datos del documento
import csv
import os
# Cargar libreriá para trabajar con fechas
import datetime
# Cargar las librerías necesaria para leer el archivo .xlsx
import openpyxl

# Declaración de constantes
EMPRESAS = ['GEOPARK', 'PAREX']
CAMPOS = ['CHIRICOCA', 'INDICO-2', 'INDICO-1X', 'AZOGUE', 'GUACO', 'ADALIA',
            'AKIRA', 'MARACAS', 'CARMENTEA', 'CALONA', 'CAPACHOS', 'JACANA ESTACION',
            'TIGANA ESTACION', 'CABRESTERO - BACANO JACANA ESTACION']
OPERACIONES = ['DESPACHO POR REMITENTE', 'RECIBO POR REMITENTE JACANA',
                'RECIBO POR REMITENTE TIGANA', 'ENTREGA POR REMITENTE']
CONDICIONES = ['GOV', 'GSV', 'NSV']

def escribir_datos(nombre_documento, cabecera, datos):
    """
    Crea un documento .csv con el nombre_documento indicado en el parámetro que recibe.

    Parámetros:
    ----------
    nombre_documento -> str - Cadena de caracteres con el nombre del documento a crear
    cabecera   -> str - Cadena de caracteres con los nombres de las columnas
    datos  -> dict - Diccionario con los datos a almacenar en el documento
    """
    # Verificar si el documento existe
    if os.path.exists(nombre_documento):
        # Si nombre_documento existe se abre en modo append ('agregar informacion')
        with open(nombre_documento, 'a',  newline='') as documento_csv:
            writer = csv.DictWriter(documento_csv, fieldnames=cabecera)
            writer.writerows(datos)
    else:
        with open(nombre_documento, 'w', newline='') as documento_csv:
            # Si el documento no existe se abre en modo escritura
            writer = csv.DictWriter(documento_csv, fieldnames=cabecera)
            writer.writeheader() # escribir la cabecera
            writer.writerows(datos)

def leer_datos(documento, inicio=1, fin=270):
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
    #Cargar el documento excel
    book = openpyxl.load_workbook(documento, data_only=True)
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
            # si valor se encuentra en la constante CAMPO guarda todos los datos
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
    La función es la encargada de limpiar los datos cuando estos no tienen el
    tipo de datos esperado, o tienen campo vacios que los hacen inválidos.

    Parámetros:
    -----------
    datos -> list - Lista de diccionarios con los datos a limpiar

    Retorna:
    --------

    """
    procesados = list()
    for dato in datos:
        # Remover los diccionarios con GVO, GSV  NSV vacíos
        float_gov = isinstance(dato['GOV'], float)
        float_gsv = isinstance(dato['GSV'], float)
        float_nsv = isinstance(dato['NSV'], float)
        if not float_gov and not float_gsv and not float_nsv:
            continue
        procesados.append(dato)
    return procesados

def registrar_procesado(reporte):
    """
    Agregar el reporte al documento de reportes procesados, en caso de que el documento
    no exista, lo creará y luego agregará el reporte. El documento reportes_procesados
    continene la fecha en la que se procesó el reporte y el nombre del reporte procesado.

    Parámetros:
    -----------
    reporte -> str - Cadena de caracteres con el nombre del reporte procesado
    """
    cabecera = ['fecha', 'nombre_reporte']
    datos = [{'fecha': datetime.date.today(), 'nombre_reporte': reporte}]
    escribir_datos('reportes_procesados.csv', cabecera, datos)

def verificar_procesados(reporte):
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
    if os.path.exists('reportes_procesados.csv'):
        with open('reportes_procesados.csv', 'r') as reportes:
            reader = csv.DictReader(reportes)
            for procesado in reader:
                if procesado['nombre_reporte'] == reporte:
                    found = True
    return found


if __name__ == "__main__":
    pass
    