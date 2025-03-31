-- clean_and_move_data.sql
CREATE OR REPLACE TABLE `dtc-de-course-447820.my_project_dataset.monitoring_locations` AS
SELECT
    `Site_ID`,
    `Location_description`,
    `Borough`,
    `Functional_area_for_monitoring`,
    `Road_type`,
    `Easting__UK_Grid_` AS `Easting_UK_Grid`,  -- Updated column name
    `Northing__UK_Grid_` AS `Northing_UK_Grid`,  -- Updated column name
    `Latitude`,
    `Longitude`
FROM `dtc-de-course-447820.my_project_dataset.raw_monitoring_locations`;
