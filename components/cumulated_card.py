from dash import html

def make_cumulated_card(company, operation_condition):
    return html.Div([
                html.H6(children=f"{company.capitalize()} {operation_condition.upper()} (bbls)"),
                html.P(id=f"{operation_condition.upper()}-acumulado-{company.lower()}"
                   )], className="card_container two columns " + f"acumulado-{company.lower()}",
                )