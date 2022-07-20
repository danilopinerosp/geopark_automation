import pandas as pd
from utils.constants import balance_data


# Cargos los datos del balance
datos = pd.read_csv(balance_data)
# Convertir las fechas al tipo de dato datatime
datos['fecha'] = pd.to_datetime(datos['fecha'], format='%d-%m-%Y')