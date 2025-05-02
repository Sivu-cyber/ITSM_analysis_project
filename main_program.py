import os
import zipfile

# Set up directory structure for the DBT project
base_dir = "/mnt/data/my_itsm_dbt_project"
os.makedirs(f"{base_dir}/models/staging", exist_ok=True)
os.makedirs(f"{base_dir}/models/marts/service_metrics", exist_ok=True)
os.makedirs(f"{base_dir}/snapshots", exist_ok=True)

# DBT files content
dbt_project_yml = """name: 'my_itsm_dbt_project'
version: '1.0'
config-version: 2

profile: 'default'

model-paths: ["models"]
snapshot-paths: ["snapshots"]

models:
  my_itsm_dbt_project:
    +materialized: view
    staging:
      +schema: staging
    marts:
      +schema: marts
"""

sources_yml = """version: 2

sources:
  - name: raw
    tables:
      - name: cleaned_ticket_data
"""

stg_cleaned_ticket_sql = """SELECT
    *
FROM {{ source('raw', 'cleaned_ticket_data') }}
"""

avg_resolution_sql = """SELECT
    inc_category,
    inc_priority,
    ROUND(AVG(resolution_time_hrs), 2) AS avg_resolution_time_hrs
FROM {{ ref('stg_cleaned_ticket_data') }}
GROUP BY inc_category, inc_priority
"""

closure_rate_sql = """SELECT
    inc_assignment_group,
    COUNT(*) FILTER (WHERE inc_state ILIKE 'Closed') * 1.0 / COUNT(*) AS closure_rate
FROM {{ ref('stg_cleaned_ticket_data') }}
GROUP BY inc_assignment_group
"""

monthly_summary_sql = """SELECT
    created_year,
    created_month,
    COUNT(*) AS total_tickets,
    ROUND(AVG(resolution_time_hrs), 2) AS avg_resolution_time_hrs,
    COUNT(*) FILTER (WHERE inc_state ILIKE 'Closed') * 1.0 / COUNT(*) AS closure_rate
FROM {{ ref('stg_cleaned_ticket_data') }}
GROUP BY created_year, created_month
ORDER BY created_year, created_month
"""

# Save all files
with open(f"{base_dir}/dbt_project.yml", "w") as f:
    f.write(dbt_project_yml)

with open(f"{base_dir}/models/staging/stg_cleaned_ticket_data.sql", "w") as f:
    f.write(stg_cleaned_ticket_sql)

with open(f"{base_dir}/models/marts/service_metrics/avg_resolution_time.sql", "w") as f:
    f.write(avg_resolution_sql)

with open(f"{base_dir}/models/marts/service_metrics/closure_rate_by_group.sql", "w") as f:
    f.write(closure_rate_sql)

with open(f"{base_dir}/models/marts/service_metrics/monthly_ticket_summary.sql", "w") as f:
    f.write(monthly_summary_sql)

with open(f"{base_dir}/models/staging/schema.yml", "w") as f:
    f.write(sources_yml)

# Zip the directory
zip_path = "/mnt/data/my_itsm_dbt_project.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, base_dir)
            zipf.write(full_path, arcname=relative_path)

zip_path
