-- models/staging/stg_companies.sql
--
-- MỤC ĐÍCH:
--     Đọc data thô từ raw_companies, làm sạch và chuẩn hóa
--     trước khi đưa vào marts (dim/fact)
--
-- STAGING LÀ GÌ?
--     Staging = bước trung gian giữa raw và warehouse
--     - Đổi tên cột cho nhất quán
--     - Lọc bỏ data không hợp lệ
--     - Cast đúng kiểu dữ liệu
--     Không làm business logic ở đây

WITH source AS (
    -- Đọc thẳng từ bảng raw trong PostgreSQL
    SELECT * FROM {{ source('raw', 'raw_companies') }}
),

cleaned AS (
    SELECT
        ticker,
        name,
        exchange,
        industry,
        is_delisted,
        updated_at
    FROM source
    -- Chỉ lấy các công ty có ticker hợp lệ
    WHERE ticker IS NOT NULL
      AND name  IS NOT NULL
)

SELECT * FROM cleaned