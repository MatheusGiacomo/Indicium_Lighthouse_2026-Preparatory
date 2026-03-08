{{ config(materialized='table', schema='silver') }}

WITH raw_data AS (
    SELECT 
        country_id,
        year::int as reference_year,
        gdp_per_capita,
        ingestion_timestamp
    FROM {{ source('raw_zone', 'world_bank_gdp') }}
)

SELECT 
    country_id,
    reference_year,
    ROUND(CAST(gdp_per_capita AS numeric), 2) as gdp_usd,
    ingestion_timestamp as processed_at
FROM raw_data
WHERE gdp_per_capita IS NOT NULL