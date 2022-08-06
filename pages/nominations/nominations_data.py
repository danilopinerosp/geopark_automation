import base64
from datetime import datetime
import io
import pandas as pd
from dash import html

from utils.functions import filter_data_by_date, load_data, load_oil_types
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
    start_date = datetime.strptime(f"01-{month}-{year}", "%d-%m-%Y")
    if month == 12:
        end_date = datetime.strptime(f"01-01-{year + 1}", "%d-%m-%Y")
    else:
        end_date = datetime.strptime(f"01-{month + 1}-{year}", "%d-%m-%Y")
    return (start_date, end_date)

def remove_entries_nominations(filepath, filename):
    (start_date, end_date) = get_date_nomination(filename)
    df = pd.read_csv(filepath)
    df['fecha'] = pd.to_datetime(df['fecha'], yearfirst=True)
    mask = (df['fecha'] < start_date) | (df['fecha'] >= end_date)
    filtered = df[mask]
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

def filter_data_nominations(data, start_date, end_date, company):
    """Return a Dataframe filtered by period time and company"""
    filtered_by_date = filter_data_by_date(data, start_date, end_date)
    filter_columns = ['fecha'] + [column for column in filtered_by_date.columns if company.lower() in column.lower()]
    filtered_by_company = filtered_by_date[filter_columns]
    return filtered_by_company

def filter_data_transported(data, start_date, end_date, company):
    transported = daily_transported_oil_type(data, start_date, end_date)
    company_keys = {'geopark': 'geopark', 'verano': 'parex'}
    # filter_columns = data[company.upper()]
    transported_by_company = transported[company_keys[company.lower()].upper()]
    transported_light_oil = calculate_light_oil(transported_by_company)
    # print(transported_light_oil)
    return transported_light_oil

def calculate_light_oil(transported_data):
    oil_types = load_oil_types()
    light_oils = list(oil_types[oil_types['Livianos'] == 'SI']['Crudo'])
    light_months = [column for column in transported_data.columns if column in light_oils]
    data_light_oil = transported_data[light_months].sum(axis=1)
    data_light_oil = data_light_oil.reset_index()
    data_light_oil['fecha'] = pd.to_datetime(data_light_oil['fecha'], yearfirst=True)
    data_light_oil.columns = ['fecha', 'livianos']

    normal_oils = list(oil_types[oil_types['Livianos'] == 'NO']['Crudo'])
    normal_months = [column for column in transported_data.columns if column in normal_oils]
    data_normal_oils = transported_data[normal_months].reset_index()
    data_normal_oils['fecha'] = pd.to_datetime(data_normal_oils['fecha'], yearfirst=True)
    result = pd.concat([data_normal_oils, data_light_oil], axis = 1)
    
    return result.loc[:,~result.columns.duplicated()].copy()
