{{ config(
    materialized='view'
) }}

SELECT
    year,
    month,
    SUM(hourly_total) AS total_hourly_count
FROM {{ ref('hourly_counts_by_functional_area') }}
GROUP BY year, month
ORDER BY year, month
