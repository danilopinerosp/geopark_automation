import pandas as pd

def load_balance_data(filename):
    """
    Load the balance data from the balance.csv file
    """
    return pd.read_csv(filename)
