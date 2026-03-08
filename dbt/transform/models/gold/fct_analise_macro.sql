{{ config(materialized='table', schema='gold') }}

WITH pib AS (
    SELECT 
        country_id,
        reference_year,
        gdp_usd
    FROM {{ ref('stg_world_bank') }}
    WHERE reference_year >= 2014 
),
mercado AS (
    SELECT 
        EXTRACT(YEAR FROM dt_referencia)::int as ano,
        AVG(vlr_petroleo_brent) as media_petroleo
    FROM {{ ref('stg_market_data') }}
    GROUP BY 1
)

SELECT 
    p.country_id,
    p.reference_year,
    p.gdp_usd,
    m.media_petroleo,
    (p.gdp_usd / NULLIF(m.media_petroleo, 0)) as ratio_pib_petroleo
FROM pib p
INNER JOIN mercado m ON p.reference_year = m.ano 
ORDER BY p.reference_year DESC