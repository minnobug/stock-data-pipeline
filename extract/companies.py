"""
extract/companies.py

MỤC ĐÍCH:
    Lấy danh sách tất cả công ty đang niêm yết trên HOSE và HNX
    từ thư viện vnstock.

DATA TRẢ VỀ:
    - ticker     : mã cổ phiếu (VD: VNM, VIC, HPG)
    - name       : tên công ty
    - exchange   : sàn giao dịch (HOSE hoặc HNX)
    - industry   : ngành
    - is_delisted: có bị hủy niêm yết không

TẦN SUẤT CHẠY:
    Cuối mỗi tháng — vì danh sách công ty ít khi thay đổi.
"""

import pandas as pd
from vnstock import Vnstock


def extract_companies(exchange: str) -> pd.DataFrame:
    """
    Lấy danh sách công ty từ một sàn cụ thể.

    Args:
        exchange: 'HOSE' hoặc 'HNX'

    Returns:
        DataFrame chứa thông tin công ty
    """
    # Khởi tạo vnstock — không cần API key, free hoàn toàn
    stock = Vnstock().stock(symbol="VNM", source="VCI")

    # Lấy toàn bộ danh sách công ty theo sàn
    # symbols_by_exchange() trả về DataFrame gồm:
    # ticker, organ_name, organ_type, exchange, ...
    df = stock.listing.symbols_by_exchange()

    # Lọc đúng sàn cần lấy
    df = df[df["exchange"] == exchange].copy()

    # Đổi tên cột cho dễ đọc và nhất quán với schema PostgreSQL
    df = df.rename(
        columns={
            "organ_name": "name",
            "organ_type": "industry",
        }
    )

    # Chỉ giữ các cột cần thiết
    df = df[["ticker", "name", "exchange", "industry"]]

    # Mặc định False vì đây là danh sách đang niêm yết
    df["is_delisted"] = False

    print(f"[companies] {exchange}: {len(df)} công ty")
    return df


def extract_all_companies() -> pd.DataFrame:
    """
    Lấy danh sách công ty từ cả HOSE và HNX, gộp thành 1 DataFrame.

    Returns:
        DataFrame chứa tất cả công ty từ HOSE + HNX
    """
    hose = extract_companies("HOSE")
    hnx = extract_companies("HNX")

    # pd.concat gộp 2 DataFrame theo chiều dọc (axis=0)
    # ignore_index=True để reset lại index từ 0
    df = pd.concat([hose, hnx], ignore_index=True)

    print(f"[companies] Tổng: {len(df)} công ty (HOSE + HNX)")
    return df


if __name__ == "__main__":
    df = extract_all_companies()
    print(df.head(10))
