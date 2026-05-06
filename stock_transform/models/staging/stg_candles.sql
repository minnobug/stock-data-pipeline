-- models/staging/stg_candles.sql
--
-- MỤC ĐÍCH:
--     Đọc data OHLC thô từ raw_candles, làm sạch và chuẩn hóa

WITH source AS (
    SELECT * FROM {{ source('raw', 'raw_candles') }}
),

cleaned AS (
    SELECT
        ticker,
        trade_date,
        open,
        high,
        low,
        close,
        volume
    FROM source
    -- Lọc bỏ các dòng có giá trị âm hoặc null
    WHERE ticker     IS NOT NULL
      AND trade_date IS NOT NULL
      AND close      > 0
      AND volume     >= 0
)

SELECT * FROM cleaned