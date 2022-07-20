import pandas as pd
from utils.functions import load_data

def get_date_last_update(data):
    """
    Return the date of the last update in the balance data
    """
    try:
        df = load_data(data)
        return df['fecha'].max().date()
    except:
        return "Aún no hay reportes"
