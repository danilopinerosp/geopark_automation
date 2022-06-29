from dash import dcc, html

def make_dash_button(text, type_button):
    """
    The function create the button component according
    to the type of it. It could be to download or to upload
    a file
    """
    # Create classname and id for the button
    id = "-".join(text.split()).lower()
    classname = type_button + " button"

    # Return a button according to the type of it
    if type_button == "upload":
        return html.Div(
                    dcc.Upload(html.Button(text, id=id, className=classname, n_clicks=0))
                )
    if type_button == "download":
        return html.Div(
                [
                html.Button(text, id=id, className=classname),
                dcc.Download(id=id)
                ])