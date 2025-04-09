{{ config(materialized='view') }}

WITH combined_data AS (
  SELECT 
    a.SiteID,
    CASE
      WHEN a.Path LIKE 'Bus lane%' THEN 'Bus lane'
      WHEN a.Path = 'Carriageway' THEN 'Carriageway'
      WHEN a.Path LIKE 'Cycle lane%' THEN 'Cycle lane'
      WHEN a.Path LIKE 'Pavement%' THEN 'Pavement'
      WHEN a.Path = 'Shared path' THEN 'Shared path'
      ELSE a.Path
    END AS Path,
    a.Mode,
    a.Count,
    a.Wave,
    b.Functional_area_for_monitoring
  FROM {{ source('staging', 'raw_cyclingdata_2023') }} a
  JOIN {{ ref('monitoring_locations_final') }} b
  ON a.SiteID = b.Site_ID

  UNION ALL

  SELECT 
    a.SiteID,
    CASE
      WHEN a.Path LIKE 'Bus lane%' THEN 'Bus lane'
      WHEN a.Path = 'Carriageway' THEN 'Carriageway'
      WHEN a.Path LIKE 'Cycle lane%' THEN 'Cycle lane'
      WHEN a.Path LIKE 'Pavement%' THEN 'Pavement'
      WHEN a.Path = 'Shared path' THEN 'Shared path'
      ELSE a.Path
    END AS Path,
    a.Mode,
    a.Count,
    a.Wave,
    b.Functional_area_for_monitoring
  FROM {{ source('staging', 'raw_cyclingdata_2024') }} a
  JOIN {{ ref('monitoring_locations_final') }} b
  ON a.SiteID = b.Site_ID
)

SELECT 
  Functional_area_for_monitoring,
  Path,
  Mode,
  Wave,
  SUM(Count) AS rental_count
FROM combined_data
GROUP BY Functional_area_for_monitoring, Path, Mode, Wave
ORDER BY rental_count DESC
