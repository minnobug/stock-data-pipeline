"""
extract/companies.py

MỤC ĐÍCH:
    Lấy danh sách tất cả công ty đang niêm yết trên HOSE và HNX
    từ thư viện vnstock 4.x.

DATA TRẢ VỀ:
    - ticker     : mã cổ phiếu (VD: VNM, VIC, HPG)
    - name       : tên công ty
    - exchange   : sàn giao dịch (HOSE hoặc HNX)
    - industry   : loại (stock, etf, ...)
    - is_delisted: có bị hủy niêm yết không

TẦN SUẤT CHẠY:
    Cuối mỗi tháng — vì danh sách công ty ít khi thay đổi.

LƯU Ý vnstock 4.x:
    symbols_by_exchange() trả về toàn bộ sàn bất kể tham số exchange.
    Phải tự filter theo cột 'exchange' sau khi lấy về.
"""

import pandas as pd
from vnstock.api.listing import Listing


def extract_all_companies() -> pd.DataFrame:
    """
    Lấy danh sách công ty từ cả HOSE và HNX.

    Returns:
        DataFrame chứa tất cả công ty từ HOSE + HNX
    """
    listing = Listing()

    # Lấy toàn bộ danh sách — vnstock 4.x không filter theo sàn
    df = listing.symbols_by_exchange(exchange="HOSE")

    # In cột thực tế để debug nếu cần
    print(f"[companies] Cột nhận được: {df.columns.tolist()}")

    # Đổi tên cột cho nhất quán với schema PostgreSQL
    df = df.rename(
        columns={
            "symbol": "ticker",
            "organ_name": "name",
            "type": "industry",
        }
    )

    # Chỉ giữ HOSE và HNX, bỏ UPCOM, XHNF, NaN
    df = df[df["exchange"].isin(["HOSE", "HNX"])].copy()

    # Thêm cột industry nếu không có (trường hợp API timeout trả về thiếu cột)
    if "industry" not in df.columns:
        print("[companies] Cảnh báo: không có cột 'industry', dùng giá trị mặc định.")
        df["industry"] = "unknown"

    # Chỉ giữ các cột cần thiết
    df = df[["ticker", "name", "exchange", "industry"]]

    # Mặc định False vì đây là danh sách đang niêm yết
    df["is_delisted"] = False

    # Reset index sau khi filter
    df = df.reset_index(drop=True)

    # In thống kê theo sàn
    for exchange in ["HOSE", "HNX"]:
        count = len(df[df["exchange"] == exchange])
        print(f"[companies] {exchange}: {count} công ty")

    print(f"[companies] Tổng: {len(df)} công ty (HOSE + HNX)")
    return df


if __name__ == "__main__":
    df = extract_all_companies()
    print(df.head(10))
    print(f"\nCác cột: {df.columns.tolist()}")
    print(f"Tổng số dòng: {len(df)}")
