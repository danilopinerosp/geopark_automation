from pydoc import classname
from dash import dash_table
import pandas as pd

def make_dash_table(daily_reports_processed):
    df = pd.read_csv(daily_reports_processed)
    df = df.dropna(axis=0)
    return dash_table.DataTable(df.to_dict('records'), 
                            [{"name": i, "id": i} for i in df.columns], 
                            id='tbl')