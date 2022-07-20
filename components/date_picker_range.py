from dash import dcc
from datetime import datetime as dt

def make_date_picker_range(id, data, date="fecha"):
    """
    Return a datePickerRange
    """
    try:
        initial_visible_month = dt(data[date].dt.year.max(),
                                    data[date].max().to_pydatetime().month, 1)
    except:
        initial_visible_month = None
    return dcc.DatePickerRange(
                id=id,
                className="date-picker-range",
                # Las fechas mínimas y máximas permitidas dependerán de las fechas
                # de los datos del balance
                min_date_allowed=data[date].min().to_pydatetime(),
                max_date_allowed=data[date].max().to_pydatetime(),
                initial_visible_month= initial_visible_month,
                # Por defecto toma como periodo de análisis los datos recolectados del último mes.
                start_date=(data[data[date].dt.month == data[date].max().month][date].min()).to_pydatetime(),
                end_date=data[date].max().to_pydatetime(),
                display_format='DD/MM/Y',
                with_portal=True,
                day_size=50
            )