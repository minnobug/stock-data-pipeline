"""
load/postgres_loader.py

MỤC ĐÍCH:
    Nhận DataFrame từ extract/ và load vào PostgreSQL (raw layer).

    Tại sao dùng "upsert" thay vì insert thông thường?
    - Nếu chạy pipeline 2 lần trong ngày, data sẽ bị trùng.
    - Upsert = INSERT ... ON CONFLICT DO NOTHING
      → Nếu dòng đã tồn tại thì bỏ qua, không báo lỗi.
      → Đảm bảo idempotent (chạy bao nhiêu lần kết quả vẫn như nhau).

CÁC HÀM CHÍNH:
    - get_connection(): kết nối PostgreSQL
    - load_companies(): upsert danh sách công ty
    - load_candles()  : insert OHLC (bỏ qua nếu đã có)
    - load_news()     : insert tin tức (bỏ qua nếu URL đã có)
"""

import os
import psycopg2
import psycopg2.extras
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """
    Tạo kết nối đến PostgreSQL từ các biến trong file .env.

    Returns:
        psycopg2 connection object
    """
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "stock_raw"),
        user=os.getenv("POSTGRES_USER", "admin"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def load_companies(df: pd.DataFrame) -> None:
    """
    Upsert danh sách công ty vào bảng raw_companies.

    Upsert = INSERT nếu chưa có, UPDATE nếu đã có.
    Dùng ticker làm khóa chính để kiểm tra trùng.

    Args:
        df: DataFrame từ extract/companies.py
    """
    if df.empty:
        print("[load] companies: DataFrame rỗng, bỏ qua.")
        return

    conn = get_connection()
    cur = conn.cursor()

    # SQL upsert:
    # INSERT INTO ... VALUES (...)
    # ON CONFLICT (ticker) → nếu ticker đã tồn tại
    # DO UPDATE SET ...    → thì cập nhật lại các cột khác
    sql = """
        INSERT INTO raw_companies (ticker, name, exchange, industry, is_delisted, updated_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        ON CONFLICT (ticker)
        DO UPDATE SET
            name        = EXCLUDED.name,
            exchange    = EXCLUDED.exchange,
            industry    = EXCLUDED.industry,
            is_delisted = EXCLUDED.is_delisted,
            updated_at  = NOW();
    """

    # Chuyển DataFrame thành list of tuples để insert hàng loạt
    records = [
        (row.ticker, row.name, row.exchange, row.industry, row.is_delisted)
        for row in df.itertuples(index=False)
    ]

    # executemany insert nhiều dòng 1 lúc, nhanh hơn loop từng dòng
    cur.executemany(sql, records)
    conn.commit()

    print(f"[load] companies: upsert {len(records)} công ty thành công.")
    cur.close()
    conn.close()


def load_candles(df: pd.DataFrame) -> None:
    """
    Insert dữ liệu OHLC vào bảng raw_candles.
    Bỏ qua nếu (ticker, trade_date) đã tồn tại.

    Args:
        df: DataFrame từ extract/vnstock_ohlc.py
    """
    if df.empty:
        print("[load] candles: DataFrame rỗng, bỏ qua.")
        return

    conn = get_connection()
    cur = conn.cursor()

    sql = """
        INSERT INTO raw_candles (ticker, trade_date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (ticker, trade_date)
        DO NOTHING;
    """

    records = [
        (row.ticker, row.trade_date, row.open, row.high, row.low, row.close, row.volume)
        for row in df.itertuples(index=False)
    ]

    cur.executemany(sql, records)
    conn.commit()

    print(f"[load] candles: insert {len(records)} dòng OHLC thành công.")
    cur.close()
    conn.close()


def load_news(df: pd.DataFrame) -> None:
    """
    Insert tin tức vào bảng raw_news.
    Bỏ qua nếu URL đã tồn tại (tránh trùng bài).

    Args:
        df: DataFrame từ extract/news_scraper.py
    """
    if df.empty:
        print("[load] news: DataFrame rỗng, bỏ qua.")
        return

    conn = get_connection()
    cur = conn.cursor()

    sql = """
        INSERT INTO raw_news (title, url, source, published_at, summary)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (url)
        DO NOTHING;
    """

    records = [
        (row.title, row.url, row.source, row.published_at, row.summary)
        for row in df.itertuples(index=False)
    ]

    cur.executemany(sql, records)
    conn.commit()

    print(f"[load] news: insert {len(records)} bài tin tức thành công.")
    cur.close()
    conn.close()


if __name__ == "__main__":
    # Test kết nối
    try:
        conn = get_connection()
        print("[load] Kết nối PostgreSQL thành công!")
        print(f"[load] Database: {conn.get_dsn_parameters()['dbname']}")
        conn.close()
    except Exception as e:
        print(f"[load] Lỗi kết nối: {e}")
