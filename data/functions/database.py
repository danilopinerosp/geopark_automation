import csv
from utils.constants import (daily_reports_processed, 
                            nominations_processed,
                            balance_data, 
                            companies,
                            oils,
                            nominations_data)

def create_csv_file(filepath, header):
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)

def init_database():
    create_csv_file(daily_reports_processed, ["fecha actualizacion", "fecha reporte"])
    create_csv_file(nominations_processed, ["fecha actualizacion", "fecha reporte"])
    create_csv_file(balance_data, ["fecha", "empresa", "operacion" , "campo", "GOV", "GSV", "NSV"])
    create_csv_file(nominations_data, ["fecha", "nominados geopark"])
    create_csv_file(companies, ["nombre"])
    create_csv_file(oils, ["Crudo", "Segmento"])

if __name__ == "__main__":
    init_database()