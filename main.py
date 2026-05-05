"""
main.py

MỤC ĐÍCH:
    Chạy toàn bộ pipeline Extract → Load.
    File này gọi lần lượt các hàm từ extract/ và load/
    để lấy data về rồi đẩy vào PostgreSQL.

CÁCH CHẠY:
    python main.py
"""

from extract.companies import extract_all_companies
from extract.vnstock_ohlc import extract_all_ohlc
from extract.news_scraper import scrape_vneconomy
from load.postgres_loader import load_companies, load_candles, load_news

# ==========================================
# CẤU HÌNH
# ==========================================

# Danh sách mã cổ phiếu cần lấy OHLC
# TODO: sau này sẽ lấy tự động từ raw_companies
TICKERS = ["VNM", "VIC", "HPG", "VHM", "VCB"]

# Khoảng thời gian lấy OHLC
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"


# ==========================================
# PIPELINE
# ==========================================


def run():
    print("=" * 50)
    print("VIETNAM STOCK DATA PIPELINE")
    print("=" * 50)

    # BƯỚC 1: Extract companies
    print("\n[1/3] Extracting companies...")
    df_companies = extract_all_companies()

    # BƯỚC 2: Extract OHLC
    print("\n[2/3] Extracting OHLC...")
    df_candles = extract_all_ohlc(TICKERS, START_DATE, END_DATE)

    # BƯỚC 3: Extract news
    print("\n[3/3] Extracting news...")
    df_news = scrape_vneconomy()

    # BƯỚC 4: Load vào PostgreSQL
    print("\n[4/4] Loading into PostgreSQL...")
    load_companies(df_companies)
    load_candles(df_candles)
    load_news(df_news)

    print("\n" + "=" * 50)
    print("PIPELINE HOÀN THÀNH!")
    print("=" * 50)


if __name__ == "__main__":
    run()
