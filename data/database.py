import sqlite3
from sqlite3 import Error


def crear_db(db_file):
    """Crear la base de datos para la applicación"""
    # Declarar la conexión a la base de datos
    conn = sqlite3.connect(db_file)
    # Declarar el cursor para poder crear las tablas
    cursor = conn.cursor()

    ## Crear las tablas para almacenar los datos de la operación

    # Crear la tabla para los campos
    cursor.execute('''CREATE TABLE IF NOT EXISTS Campos (
        id_campo INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        segmento TEXT NOT NULL,
        llanos TEXT NOT NULL,
        livianos TEXT NOT NULL);       
        ''')
    
    # Crear la tabla para los reportes procesados
    cursor.execute('''CREATE TABLE IF NOT EXISTS Reportes_procesados (
        id_reporte INTEGER PRIMARY KEY,
        fecha_procesamiento TEXT NOT NULL,
        fecha_reporte TEXT NOT NULL);
        ''')

    # Crear la tabla para el balance
    cursor.execute('''CREATE TABLE IF NOT EXISTS Balance (
        id_balance INTEGER PRIMARY KEY,
        fecha TEXT NOT NULL,
        empresa TEXT NOT NULL,
        operacion TEXT NOT NULL,
        id_campo INTEGER,
        GOV REAL,
        GSV REAL,
        NSV REAL);
        ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_db(r"data/auto_geopark.db")