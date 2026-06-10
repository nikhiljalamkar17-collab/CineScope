import pandas as pd

def load_all_data():
    file = "data/data.xlsx"
    return {
        "movies": pd.read_excel(file, sheet_name="Movie Data"),
        "food": pd.read_excel(file, sheet_name="Food &Bev"),
        "employees": pd.read_excel(file, sheet_name="Employee Data"),
        "theaters": pd.read_excel(file, sheet_name="Theaters Data"),
        "visitors": pd.read_excel(file, sheet_name="Visitors Data")
    }