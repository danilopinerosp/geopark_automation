import pandas as pd


# Cargos los datos del balance
datos = pd.read_csv('data/balance.csv')
# Convertir las fechas al tipo de dato datatime
datos['fecha'] = pd.to_datetime(datos['fecha'], format='%d-%m-%Y')