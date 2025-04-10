{{ config(
    materialized='view'
) }}

WITH combined_data AS (
    SELECT
        ml.Functional_area_for_monitoring AS functional_area,
        CAST(SUBSTRING(cd.Wave, 1, 4) AS INT64) AS year,
        EXTRACT(MONTH FROM cd.Date) AS month,
        EXTRACT(HOUR FROM TIME(cd.Time)) AS numeric_hour,
        CONCAT(
            FORMAT("%02d", EXTRACT(HOUR FROM TIME(cd.Time))), 
            '-', 
            FORMAT("%02d", EXTRACT(HOUR FROM TIME(cd.Time)) + 1)
        ) AS hour_range,
        SUM(cd.Count) AS total_count
    FROM {{ source('staging', 'raw_cyclingdata_2023') }} cd
    JOIN {{ ref('monitoring_locations') }} ml
        ON cd.SiteID = ml.Site_ID
    GROUP BY functional_area, year, month, numeric_hour, hour_range

    UNION ALL

    SELECT
        ml.Functional_area_for_monitoring AS functional_area,
        CAST(SUBSTRING(cd.Wave, 1, 4) AS INT64) AS year,
        EXTRACT(MONTH FROM cd.Date) AS month,
        EXTRACT(HOUR FROM TIME(cd.Time)) AS numeric_hour,
        CONCAT(
            FORMAT("%02d", EXTRACT(HOUR FROM TIME(cd.Time))), 
            '-', 
            FORMAT("%02d", EXTRACT(HOUR FROM TIME(cd.Time)) + 1)
        ) AS hour_range,
        SUM(cd.Count) AS total_count
    FROM {{ source('staging', 'raw_cyclingdata_2024') }} cd
    JOIN {{ ref('monitoring_locations') }} ml
        ON cd.SiteID = ml.Site_ID
    GROUP BY functional_area, year, month, numeric_hour, hour_range
)

SELECT 
    functional_area,
    year,
    month,
    numeric_hour,
    hour_range,
    SUM(total_count) AS hourly_total
FROM combined_data
GROUP BY functional_area, year, month, numeric_hour, hour_range
ORDER BY functional_area, year, month, numeric_hour
