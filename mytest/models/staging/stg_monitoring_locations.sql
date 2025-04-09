{{ config(materialized='view') }}

SELECT
  Site_ID,
  Location_description,
  Borough,
  Functional_area_for_monitoring,
  Road_type,
  Easting__UK_Grid_ AS Easting_UK_Grid,
  Northing__UK_Grid_ AS Northing_UK_Grid,
  Latitude,
  Longitude
FROM {{ source('staging', 'raw_monitoring_locations') }}

