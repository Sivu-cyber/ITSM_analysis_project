import pandas as pd

# Load the Excel file and show the sheet names
excel_path = "/mnt/data/Sample Data file for Analysis_Jan'25.xlsx"
xls = pd.ExcelFile(excel_path)

# Display sheet names
xls.sheet_names
