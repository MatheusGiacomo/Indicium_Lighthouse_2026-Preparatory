{{ config(materialized='table', schema='silver') }}

SELECT 
    reference_date::date as dt_referencia,
    "bvsp" as vlr_ibovespa,
    "cl" as vlr_petroleo_brent,
    "gc" as vlr_ouro,
    ingestion_timestamp as processado_em
FROM {{ source('raw_zone', 'market_commodities') }}
WHERE "bvsp" IS NOT NULL