from turtle import ht
from dash import dcc, html

def make_dash_button(text, id, type_button):
    """
    The function create the button component according
    to the type of it. It could be to download or to upload
    a file
    """
    if type_button == "upload":
        return dcc.Upload(html.Button(text, id=id, n_clicks=0))
    if type_button == "download":
        return dcc.Download(html.Button(text, id=id))