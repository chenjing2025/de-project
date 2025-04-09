{{ config(materialized='table') }}

SELECT *
FROM {{ ref('stg_monitoring_locations') }}

