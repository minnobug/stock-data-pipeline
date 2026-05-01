"""
extract/news_scraper.py

MỤC ĐÍCH:
    Scrape tin tức tài chính từ CafeF — trang tin tức chứng khoán
    lớn nhất Việt Nam.

    "Scraping" là kỹ thuật đọc nội dung HTML của trang web
    rồi trích xuất thông tin cần thiết bằng code.
    Khác với API (có endpoint rõ ràng), scraping phải
    tự tìm đúng thẻ HTML chứa data.

DATA TRẢ VỀ:
    - title       : tiêu đề bài viết
    - url         : đường link bài viết
    - source      : nguồn (CafeF)
    - published_at: thời gian đăng
    - summary     : tóm tắt nội dung

TẦN SUẤT CHẠY:
    Mỗi ngày — lấy tin tức mới nhất về thị trường.

LƯU Ý:
    Scraping phụ thuộc vào cấu trúc HTML của trang web.
    Nếu CafeF thay đổi giao diện, code có thể cần cập nhật.
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


# URL danh mục chứng khoán của CafeF
CAFEF_URL = "https://cafef.vn/thi-truong-chung-khoan.chn"

# Header để giả lập browser — một số trang chặn request không có header
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def scrape_cafef(pages: int = 3) -> pd.DataFrame:
    """
    Scrape tin tức chứng khoán từ CafeF.

    Args:
        pages: số trang cần scrape (mỗi trang ~20 bài)

    Returns:
        DataFrame với các cột: title, url, source, published_at, summary

    Cách hoạt động:
        1. Gửi HTTP GET request đến CafeF
        2. Đọc HTML trả về bằng BeautifulSoup
        3. Tìm các thẻ chứa tin tức (thẻ <a>, <h3>, <p>...)
        4. Trích xuất title, url, summary từ các thẻ đó
        5. Trả về DataFrame
    """
    all_articles = []

    for page in range(1, pages + 1):
        # Tạo URL cho từng trang
        # CafeF dùng query param ?page=N để phân trang
        url = f"{CAFEF_URL}?page={page}"

        try:
            # Gửi request đến CafeF, timeout=10 giây
            response = requests.get(url, headers=HEADERS, timeout=10)

            # Kiểm tra request có thành công không (status 200 = OK)
            response.raise_for_status()

            # Parse HTML bằng BeautifulSoup
            # 'html.parser' là parser mặc định của Python, không cần cài thêm
            soup = BeautifulSoup(response.text, "html.parser")

            # Tìm tất cả block tin tức trên trang
            # Cần inspect HTML của CafeF để tìm đúng class
            # Đây là class phổ biến của CafeF — có thể cần điều chỉnh
            articles = soup.find_all("div", class_="item")

            for article in articles:
                try:
                    # Lấy tiêu đề và link từ thẻ <a> trong <h3>
                    title_tag = article.find("h3")
                    if not title_tag:
                        continue

                    link_tag = title_tag.find("a")
                    if not link_tag:
                        continue

                    title = link_tag.get_text(strip=True)
                    article_url = link_tag.get("href", "")

                    # Nếu URL là relative (không có http) thì thêm domain vào
                    if article_url.startswith("/"):
                        article_url = f"https://cafef.vn{article_url}"

                    # Lấy tóm tắt từ thẻ <p> hoặc <div class="sapo">
                    summary_tag = article.find("p") or article.find(
                        "div", class_="sapo"
                    )
                    summary = summary_tag.get_text(strip=True) if summary_tag else ""

                    all_articles.append(
                        {
                            "title": title,
                            "url": article_url,
                            "source": "CafeF",
                            "published_at": datetime.now(),  # CafeF không luôn có timestamp rõ
                            "summary": summary,
                        }
                    )

                except Exception as e:
                    # Bỏ qua bài lỗi, tiếp tục bài tiếp theo
                    print(f"[news] Lỗi parse bài: {e}")
                    continue

            print(f"[news] Trang {page}: lấy được {len(articles)} bài")

        except requests.RequestException as e:
            print(f"[news] Lỗi request trang {page}: {e}")
            continue

    if not all_articles:
        print("[news] Không lấy được tin tức nào!")
        return pd.DataFrame()

    df = pd.DataFrame(all_articles)

    # Xóa các bài trùng URL
    df = df.drop_duplicates(subset="url")

    print(f"[news] Tổng: {len(df)} bài sau khi lọc trùng")
    return df


if __name__ == "__main__":
    df = scrape_cafef(pages=2)
    print(df.head(5))
    print(f"\nCác cột: {df.columns.tolist()}")
    print(f"Tổng số dòng: {len(df)}")
