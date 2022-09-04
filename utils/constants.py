conditions = ['GOV', 'GSV', 'NSV']

operations = ['DESPACHO POR REMITENTE', 'RECIBO POR REMITENTE JACANA',
                'RECIBO POR REMITENTE TIGANA', 'ENTREGA POR REMITENTE']

# Location of pages
balance_page_location = "/"
nominations_page_location = "/nominations"
reports_page_location = "/reports"
upload_page_location = "/upload"

# location of data
balance_data = "data/consolidated_data/balance.csv"
nominations_data = "data/consolidated_data/nominations.csv"
companies = "data/consolidated_data/companies.csv"
oils = "data/consolidated_data/oils.csv"
daily_reports_processed = "data/log_data/daily_reports_processed.csv"
nominations_processed = "data/log_data/nominations_processed.csv"

# Months
months = ['Enero', 
        'Febrero',
        'Marzo',
        'Abril', 
        'Mayo', 
        'Junio', 
        'Julio', 
        'Agosto', 
        'Septiembre', 
        'Octubre',
        'Noviembre',
        'Diciembre']


# Header
header_nominations = ['fecha', 
                'nominado jacana geopark',
                'nominado tigana geopark', 
                'nominado livianos geopark', 
                'nominado cabrestero verano', 
                'nominado jacana verano', 
                'nominado tigana verano', 
                'nominado livianos verano']

parex = [
    "ACUMULADO MENSUAL CABRESTERO - BACANO",
    "ACUMULADO MENSUAL MARACAS",
    "ACUMULADO MENSUAL INDICO 1",
    "ACUMULADO MENSUAL INDICO 2",
    "ACUMULADO MENSUAL ADALIA",
    "ACUMULADO MENSUAL CAPACHOS",
]