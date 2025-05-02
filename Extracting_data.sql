# Generate DBT model SQLs as strings for three transformations

# 1. Average resolution time per Category and Priority
avg_resolution_sql = """
SELECT
    inc_category,
    inc_priority,
    ROUND(AVG(resolution_time_hrs), 2) AS avg_resolution_time_hrs
FROM {{ ref('cleaned_ticket_data') }}
GROUP BY inc_category, inc_priority
"""

# 2. Ticket closure rate per Assigned Group
closure_rate_sql = """
SELECT
    inc_assignment_group,
    COUNT(*) FILTER (WHERE inc_state ILIKE 'Closed') * 1.0 / COUNT(*) AS closure_rate
FROM {{ ref('cleaned_ticket_data') }}
GROUP BY inc_assignment_group
"""

# 3. Monthly Ticket Summary
monthly_summary_sql = """
SELECT
    created_year,
    created_month,
    COUNT(*) AS total_tickets,
    ROUND(AVG(resolution_time_hrs), 2) AS avg_resolution_time_hrs,
    COUNT(*) FILTER (WHERE inc_state ILIKE 'Closed') * 1.0 / COUNT(*) AS closure_rate
FROM {{ ref('cleaned_ticket_data') }}
GROUP BY created_year, created_month
ORDER BY created_year, created_month
"""

avg_resolution_sql, closure_rate_sql, monthly_summary_sql
