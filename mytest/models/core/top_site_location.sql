{{ config(
    materialized='view'
) }}

WITH combined_data AS (
    SELECT
        cd.SiteID,
        ml.Functional_area_for_monitoring AS functional_area,
        CAST(SUBSTRING(cd.Wave, 1, 4) AS INT64) AS year,  
        SUM(cd.Count) AS total_count
    FROM {{ source('staging', 'raw_cyclingdata_2023') }} cd
    JOIN {{ ref('monitoring_locations') }} ml
        ON cd.SiteID = ml.Site_ID
    GROUP BY cd.SiteID, ml.Functional_area_for_monitoring, year

    UNION ALL  

    SELECT
        cd.SiteID,
        ml.Functional_area_for_monitoring AS functional_area,
        CAST(SUBSTRING(cd.Wave, 1, 4) AS INT64) AS year,  
        SUM(cd.Count) AS total_count
    FROM {{ source('staging', 'raw_cyclingdata_2024') }} cd
    JOIN {{ ref('monitoring_locations') }} ml
        ON cd.SiteID = ml.Site_ID
    GROUP BY cd.SiteID, ml.Functional_area_for_monitoring, year
),

ranked_sites AS (
    SELECT
        SiteID,
        functional_area,
        year,
        total_count,
        ROW_NUMBER() OVER (PARTITION BY year, functional_area ORDER BY total_count DESC) AS rank 
    FROM combined_data
)

SELECT
    rs.SiteID,
    rs.functional_area,
    ml.Location_description,
    rs.year,
    rs.total_count
FROM ranked_sites rs
JOIN {{ ref('monitoring_locations') }} ml
    ON rs.SiteID = ml.Site_ID
WHERE rank <= 3
ORDER BY rs.year, rs.functional_area, rs.total_count DESC
