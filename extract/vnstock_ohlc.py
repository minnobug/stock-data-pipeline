"""
extract/vnstock_ohlc.py

MỤC ĐÍCH:
    Lấy dữ liệu giá cổ phiếu hàng ngày (OHLC) từ vnstock 4.x.

    OHLC là viết tắt của:
        O - Open  : giá mở cửa
        H - High  : giá cao nhất trong ngày
        L - Low   : giá thấp nhất trong ngày
        C - Close : giá đóng cửa
    + Volume: khối lượng giao dịch

DATA TRẢ VỀ:
    - ticker    : mã cổ phiếu
    - trade_date: ngày giao dịch
    - open      : giá mở cửa
    - high      : giá cao nhất
    - low       : giá thấp nhất
    - close     : giá đóng cửa
    - volume    : khối lượng giao dịch

TẦN SUẤT CHẠY:
    Mỗi ngày sau khi thị trường đóng cửa (khoảng 15:30).

LƯU Ý vnstock 4.x:
    Dùng vnstock.api.quote.Quote thay vì Vnstock().stock()
    Cột thời gian là 'time', không phải 'date' hay 'trade_date'
"""

import pandas as pd
from vnstock.api.quote import Quote


def extract_ohlc(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Lấy dữ liệu OHLC của một mã cổ phiếu trong khoảng thời gian.

    Args:
        ticker    : mã cổ phiếu, VD: 'VNM', 'VIC', 'HPG'
        start_date: ngày bắt đầu, định dạng 'YYYY-MM-DD'
        end_date  : ngày kết thúc, định dạng 'YYYY-MM-DD'

    Returns:
        DataFrame với các cột: ticker, trade_date, open, high, low, close, volume

    Ví dụ:
        df = extract_ohlc('VNM', '2024-01-01', '2024-12-31')
    """
    # Khởi tạo Quote API của vnstock 4.x
    q = Quote(symbol=ticker, source="VCI")

    # Lấy lịch sử giá theo ngày
    # interval='1D' = mỗi ngày
    df = q.history(start=start_date, end=end_date, interval="1D")

    # Đổi tên cột 'time' thành 'trade_date' cho nhất quán với schema
    df = df.rename(columns={"time": "trade_date"})

    # Thêm cột ticker vì vnstock không tự thêm
    df["ticker"] = ticker

    # Chỉ giữ các cột cần thiết, đúng thứ tự
    df = df[["ticker", "trade_date", "open", "high", "low", "close", "volume"]]

    return df


def extract_all_ohlc(tickers: list, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Lấy OHLC cho danh sách nhiều mã cổ phiếu.

    Args:
        tickers   : danh sách mã cổ phiếu, VD: ['VNM', 'VIC', 'HPG']
        start_date: ngày bắt đầu
        end_date  : ngày kết thúc

    Returns:
        DataFrame chứa OHLC của tất cả mã
    """
    all_data = []

    for ticker in tickers:
        try:
            df = extract_ohlc(ticker, start_date, end_date)
            all_data.append(df)
            print(f"[ohlc] {ticker}: {len(df)} ngày")

        except Exception as e:
            # Nếu 1 mã bị lỗi thì bỏ qua, không dừng toàn bộ
            print(f"[ohlc] {ticker}: LỖI - {e}")
            continue

    if not all_data:
        print("[ohlc] Không lấy được data nào!")
        return pd.DataFrame()

    result = pd.concat(all_data, ignore_index=True)
    print(f"[ohlc] Tổng: {len(result)} dòng từ {len(all_data)} mã")
    return result


if __name__ == "__main__":
    # Test với 3 mã lớn
    tickers = ["VNM", "VIC", "HPG"]
    df = extract_all_ohlc(tickers, "2024-01-01", "2024-01-31")
    print(df.head(10))
    print(f"\nCác cột: {df.columns.tolist()}")
    print(f"Tổng số dòng: {len(df)}")
