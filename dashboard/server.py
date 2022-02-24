import dash
import pandas as pd

# Declarar el objeto app para el dashboard
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

# Cargos los datos del balance
datos = pd.read_csv('data/balance.csv')
# Convertir las fechas al tipo de dato datatime
datos['fecha'] = pd.to_datetime(datos['fecha'], format='%d-%m-%Y')