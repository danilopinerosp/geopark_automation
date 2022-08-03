import base64
from datetime import datetime
import io
import pandas as pd
from dash import html

from utils.functions import filter_data_by_date, load_data
from utils.constants import months

def daily_transported_oil_type(data, start_date, end_date):
    """
    Return a DataFrame with the oils transported daily by oil type

    Parameters:
    -----------
    data: dataframe -> Dataframe with the production data

    Return:
    -------
    dataframe -> NSV transported daily by each oil type
    """

    filtered_data = filter_data_by_date(data, start_date, end_date)

    # Get just the transported oil of NSV
    transported = filtered_data[filtered_data['operacion'] == "DESPACHO POR REMITENTE"][['fecha', 'empresa', 'tipo crudo', 'NSV']]
    transported_oil_type = transported.pivot_table(values="NSV", 
                                                index=data["fecha"], 
                                                columns=["empresa", "tipo crudo"]
                                                ).reset_index()
    #transported_oil_type.reset_index(inplace=True)
    transported_oil_type["fecha"] = transported_oil_type['fecha'].dt.date
    transported_oil_type.set_index("fecha", inplace=True)
    transported_oil_type.fillna(0, inplace=True)
    return transported_oil_type

def get_date_nomination(filename):
    month_name = filename.split('_')[1].split('.')[0]
    month = months.index(month_name) + 1
    year = filename.split('_')[1].split('.')[1]
    start_date = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")
    if month == 12:
        end_date = datetime.strptime(f"{year + 1}-01-01", "%Y-%m-%d")
    else:
        end_date = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")
    return (start_date, end_date)

def remove_entries_nominations(filepath, filename):
    (start_date, end_date) = get_date_nomination(filename)
    df = load_data(filepath)
    filtered = df[(df['fecha'] < start_date) | (df[df['fecha'] >= end_date])]
    return filtered
    

def parse_contents(contents, filename, date, header):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    if 'xls' in filename:
        df = pd.read_excel(io.BytesIO(decoded), 
                            names=header, 
                            skiprows=4,
                            nrows=31).reset_index(drop=True)
        return df.dropna(how='all').fillna(0)
    return pd.DataFrame()

def clean_nominations_data(s):
    pass
