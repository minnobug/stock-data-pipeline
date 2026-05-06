-- models/marts/fact_candles.sql
--
-- MỤC ĐÍCH:
--     Bảng fact chứa dữ liệu OHLC hàng ngày
--     Join với dim_companies và dim_times để phân tích
--
-- BUSINESS REQUIREMENTS ĐÁP ỨNG:
--     BR1: Phân tích xu hướng giá cổ phiếu
--     BR3: Phân tích khối lượng giao dịch
--     BR4: Phân tích theo nhóm ngành

WITH candles AS (
    SELECT * FROM {{ ref('stg_candles') }}
),

companies AS (
    SELECT * FROM {{ ref('dim_companies') }}
),

times AS (
    SELECT * FROM {{ ref('dim_times') }}
)

SELECT
    -- Keys
    candles.ticker                  AS company_id,
    candles.trade_date              AS date_id,

    -- Company info (denormalized để query nhanh hơn)
    companies.name                  AS company_name,
    companies.exchange,
    companies.industry,

    -- Time info
    times.day_of_week,
    times.day,
    times.month,
    times.quarter,
    times.year,

    -- OHLC metrics
    candles.open,
    candles.high,
    candles.low,
    candles.close,
    candles.volume,

    -- Calculated metrics
    candles.close - candles.open                        AS price_change,
    ROUND(
        ((candles.close - candles.open) / NULLIF(candles.open, 0) * 100)::NUMERIC
    , 2)                                                AS price_change_pct

FROM candles
LEFT JOIN companies ON candles.ticker    = companies.ticker
LEFT JOIN times     ON candles.trade_date = times.trade_date