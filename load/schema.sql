-- ==========================================
-- RAW LAYER — Vietnam Stock Data Pipeline
-- Chạy tự động khi Docker khởi động lần đầu
-- ==========================================

-- Bảng lưu danh sách công ty niêm yết trên HOSE và HNX
CREATE TABLE IF NOT EXISTS raw_companies (
    ticker          VARCHAR(20) PRIMARY KEY,   -- mã cổ phiếu, VD: VNM
    name            VARCHAR(255),              -- tên công ty
    exchange        VARCHAR(20),               -- HOSE hoặc HNX
    industry        VARCHAR(100),              -- loại: stock, etf, ...
    is_delisted     BOOLEAN DEFAULT FALSE,     -- đã bị hủy niêm yết chưa
    updated_at      TIMESTAMP DEFAULT NOW()    -- lần cập nhật cuối
);

-- Bảng lưu giá cổ phiếu hàng ngày (OHLC)
CREATE TABLE IF NOT EXISTS raw_candles (
    id              SERIAL PRIMARY KEY,
    ticker          VARCHAR(20),               -- mã cổ phiếu
    trade_date      DATE,                      -- ngày giao dịch
    open            NUMERIC(18, 2),            -- giá mở cửa
    high            NUMERIC(18, 2),            -- giá cao nhất
    low             NUMERIC(18, 2),            -- giá thấp nhất
    close           NUMERIC(18, 2),            -- giá đóng cửa
    volume          BIGINT,                    -- khối lượng giao dịch
    inserted_at     TIMESTAMP DEFAULT NOW(),   -- thời gian insert vào DB

    -- Đảm bảo không có 2 dòng cùng ticker + ngày
    -- Nếu đã có thì bỏ qua, không báo lỗi
    UNIQUE (ticker, trade_date)
);

-- Bảng lưu tin tức tài chính
CREATE TABLE IF NOT EXISTS raw_news (
    id              SERIAL PRIMARY KEY,
    title           TEXT,                      -- tiêu đề bài viết
    url             TEXT UNIQUE,               -- link bài viết (unique để tránh trùng)
    source          VARCHAR(100),              -- nguồn: VnEconomy, CafeF, ...
    published_at    TIMESTAMP,                 -- thời gian đăng bài
    summary         TEXT,                      -- tóm tắt nội dung
    inserted_at     TIMESTAMP DEFAULT NOW()
);

-- Index giúp query nhanh hơn khi filter theo ticker + ngày
CREATE INDEX IF NOT EXISTS idx_candles_ticker_date ON raw_candles (ticker, trade_date);

-- Index giúp query nhanh hơn khi filter tin tức theo ngày
CREATE INDEX IF NOT EXISTS idx_news_published ON raw_news (published_at);