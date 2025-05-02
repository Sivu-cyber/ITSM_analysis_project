import numpy as np

# Prepare cleaned DataFrame for export
df_cleaned = df.copy()

# Step 1: Drop duplicate records
df_cleaned = df_cleaned.drop_duplicates()

# Step 2: Handle missing values
# Drop rows where key identifiers are missing
df_cleaned = df_cleaned.dropna(subset=['inc_number', 'inc_sys_created_on', 'inc_resolved_at'])

# Step 3: Standardize date formats
df_cleaned['inc_sys_created_on'] = pd.to_datetime(df_cleaned['inc_sys_created_on'], errors='coerce')
df_cleaned['inc_resolved_at'] = pd.to_datetime(df_cleaned['inc_resolved_at'], errors='coerce')

# Step 4: Calculate resolution time in hours
df_cleaned['resolution_time_hrs'] = (df_cleaned['inc_resolved_at'] - df_cleaned['inc_sys_created_on']).dt.total_seconds() / 3600

# Step 5: Extract Year, Month, Day from created date
df_cleaned['created_year'] = df_cleaned['inc_sys_created_on'].dt.year
df_cleaned['created_month'] = df_cleaned['inc_sys_created_on'].dt.month
df_cleaned['created_day'] = df_cleaned['inc_sys_created_on'].dt.day

# Export cleaned dataset to CSV for loading into Postgres
csv_path = "/mnt/data/cleaned_ticket_data.csv"
df_cleaned.to_csv(csv_path, index=False)

csv_path
