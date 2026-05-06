-- models/marts/fact_news.sql
--
-- MỤC ĐÍCH:
--     Bảng fact chứa tin tức tài chính
--     Dùng để phân tích sentiment thị trường
--
-- BUSINESS REQUIREMENTS ĐÁP ỨNG:
--     BR2: Phân tích sentiment thị trường từ tin tức

WITH news AS (
    SELECT * FROM {{ ref('stg_news') }}
)

SELECT
    id                                          AS news_id,
    title,
    url,
    source,
    published_at,
    summary,

    -- Time dimensions
    EXTRACT(DOW     FROM published_at)::INT     AS day_of_week,
    EXTRACT(DAY     FROM published_at)::INT     AS day,
    EXTRACT(MONTH   FROM published_at)::INT     AS month,
    EXTRACT(QUARTER FROM published_at)::INT     AS quarter,
    EXTRACT(YEAR    FROM published_at)::INT     AS year

FROM news