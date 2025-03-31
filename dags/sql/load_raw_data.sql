CREATE OR REPLACE EXTERNAL TABLE `dtc-de-course-447820.my_project_dataset.external_raw_data`
OPTIONS (
  format = 'CSV',
  uris = ['gs://my-deproject-data-bucket/test_cycle/monitoring_locations.csv'],
  skip_leading_rows = 1  -- Skips header row if present
);

-- Create or replace the raw table in BigQuery using data from the external table
CREATE OR REPLACE TABLE `dtc-de-course-447820.my_project_dataset.raw_monitoring_locations` AS
SELECT
    `Site_ID`,
    `Location_description`,
    `Borough`,
    `Functional_area_for_monitoring`,
    `Road_type`,
    `Is_it_on_the_strategic_CIO_panel_`,  -- Check for the correct column name here
    `Old_site_ID__legacy_`,  -- Adjusted column name with extra underscores
    `Easting__UK_Grid_`,  -- Updated column name
    `Northing__UK_Grid_`,  -- Updated column name
    `Latitude`,
    `Longitude`
FROM `dtc-de-course-447820.my_project_dataset.external_raw_data`;
