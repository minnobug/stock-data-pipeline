-- models/marts/dim_companies.sql
--
-- MỤC ĐÍCH:
--     Bảng dimension chứa thông tin công ty
--     Dùng để join với fact_candles và fact_news

WITH stg AS (
    SELECT * FROM {{ ref('stg_companies') }}
)

SELECT
    ticker                          AS company_id,
    ticker,
    name,
    exchange,
    industry,
    is_delisted,
    updated_at
FROM stg