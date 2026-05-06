-- models/staging/stg_news.sql
--
-- MỤC ĐÍCH:
--     Đọc tin tức thô từ raw_news, làm sạch và chuẩn hóa

WITH source AS (
    SELECT * FROM {{ source('raw', 'raw_news') }}
),

cleaned AS (
    SELECT
        id,
        title,
        url,
        source,
        published_at,
        summary
    FROM source
    WHERE title        IS NOT NULL
      AND url          IS NOT NULL
      AND published_at IS NOT NULL
)

SELECT * FROM cleaned