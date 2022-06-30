from pydoc import classname
from dash import dash_table

def make_dash_table(df):
    df = df.dropna(axis=0)
    return dash_table.DataTable(df.to_dict('records'), 
                            [{"name": i, "id": i} for i in df.columns], 
                            id='tbl')