# Importar layout
# from layouts.layout import layout
from layouts.layout_app import layout
# Importar todos los callbacks
from callbacks.visualizations import *
from callbacks.values import *


# Definir el layout del dashboard
app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)
