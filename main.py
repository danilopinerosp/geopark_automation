import os
from data.get_data import (
    leer_datos, escribir_datos, 
    limpiar_datos, 
    registrar_procesado, 
    verificar_procesados,
)

def main():
    # Nombres de los valores a guardar en el balance
    cabecera = ['fecha', 'empresa', 'operacion', 'campo', 'GOV', 'GSV', 'NSV']
    # Obtener la ruta del directorio reportes
    reportes = os.path.abspath('./JULIO')
    # Procesar cada reporte que se encuentra en la ruta reportes
    for reporte in os.listdir(reportes):
        # Verificar si el reporte ya fue procesado
        if not verificar_procesados(reporte):
            # Procesar el reporte si aún no ha sido procesado
            ruta = os.path.join(reportes, reporte)
            datos = leer_datos(ruta, 1, 270)
            escribir_datos('data/consolidated_data/balance.csv', cabecera, limpiar_datos(datos))
            # Registrar el reporte que ya ha sido procesado correctamente
            registrar_procesado(reporte)


if __name__ == "__main__":
    main()