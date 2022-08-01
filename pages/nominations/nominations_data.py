import base64
import io
import pandas as pd
from dash import html

from utils.functions import filter_data_by_date

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
    print(transported_oil_type['GEOPARK'].columns)

    return transported_oil_type

def get_date_nomination(filename):
    month = filename.split('_')[1].split('.')[0]
    year = filename.split('_')[1].split('.')[1]
    return (month, year)

def remove_entries_nominations(filepath, filename):
    get_date_nomination(filename)

def parse_contents(contents, filename, date, header):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    if 'xls' in filename:
        return pd.read_excel(io.BytesIO(decoded), 
                            names=header, 
                            skiprows=4,
                            nrows=31)
    return -1

def clean_nominations_data(s):
    pass
