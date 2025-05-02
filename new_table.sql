CREATE TABLE tickets (
    inc_business_service TEXT,
    inc_category TEXT,
    inc_number TEXT PRIMARY KEY,
    inc_priority TEXT,
    inc_sla_due TEXT,
    inc_sys_created_on TIMESTAMP,
    inc_resolved_at TIMESTAMP,
    inc_assigned_to TEXT,
    inc_state TEXT,
    inc_cmdb_ci TEXT,
    inc_caller_id TEXT,
    inc_short_description TEXT,
    inc_assignment_group TEXT,
    inc_close_code TEXT,
    inc_close_notes TEXT,
    resolution_time_hrs DOUBLE PRECISION,
    created_year INT,
    created_month INT,
    created_day INT
);

-- Load CSV into Postgres (adjust file path and permissions accordingly)
COPY tickets FROM '/path/to/cleaned_ticket_data.csv' DELIMITER ',' CSV HEADER;
