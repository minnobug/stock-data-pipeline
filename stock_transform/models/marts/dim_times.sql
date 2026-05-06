-- models/marts/dim_times.sql
--
-- MỤC ĐÍCH:
--     Bảng dimension thời gian
--     Tạo từ các ngày giao dịch có trong raw_candles
--     Dùng để phân tích theo ngày, tuần, tháng, quý, năm

WITH dates AS (
    -- Lấy tất cả các ngày giao dịch unique từ raw_candles
    SELECT DISTINCT trade_date FROM {{ source('raw', 'raw_candles') }}
)

SELECT
    trade_date                              AS date_id,
    trade_date,
    EXTRACT(DOW   FROM trade_date)::INT     AS day_of_week,   -- 0=CN, 1=T2, ..., 6=T7
    EXTRACT(DAY   FROM trade_date)::INT     AS day,
    EXTRACT(MONTH FROM trade_date)::INT     AS month,
    EXTRACT(QUARTER FROM trade_date)::INT   AS quarter,
    EXTRACT(YEAR  FROM trade_date)::INT     AS year,
    TO_CHAR(trade_date, 'Month')            AS month_name,
    TO_CHAR(trade_date, 'Day')              AS day_name
FROM dates
ORDER BY trade_date