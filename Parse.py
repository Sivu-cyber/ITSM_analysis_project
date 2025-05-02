# Load the 'Raw Data' sheet to inspect the structure
df = xls.parse('Raw Data')

# Display the first few rows and column names
df.head(), df.columns.tolist()
