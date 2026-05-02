"""
extract/news_scraper.py

MỤC ĐÍCH:
    Lấy tin tức tài chính và chứng khoán từ VnEconomy RSS feed.

    Tại sao dùng RSS thay vì scraping HTML?
    - CafeF dùng JavaScript để load tin tức (dynamic rendering)
      nên BeautifulSoup không đọc được nội dung thật.
    - RSS là định dạng XML tĩnh, trả về data ngay không cần JS.
    - VnEconomy cung cấp RSS chứng khoán ổn định và miễn phí.

DATA TRẢ VỀ:
    - title       : tiêu đề bài viết
    - url         : đường link bài viết
    - source      : nguồn (VnEconomy)
    - published_at: thời gian đăng
    - summary     : tóm tắt nội dung

TẦN SUẤT CHẠY:
    Mỗi ngày — lấy tin tức mới nhất về thị trường chứng khoán.
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from email.utils import parsedate_to_datetime


# RSS feed chứng khoán của VnEconomy
VNECONOMY_RSS = "https://vneconomy.vn/chung-khoan.rss"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def parse_pubdate(pubdate_str: str) -> datetime:
    """
    Parse chuỗi ngày tháng từ RSS sang datetime.

    RSS dùng định dạng RFC 2822, VD:
        'Fri, 02 May 2025 10:30:00 +0700'

    Args:
        pubdate_str: chuỗi ngày tháng từ RSS

    Returns:
        datetime object, hoặc datetime.now() nếu parse thất bại
    """
    try:
        return parsedate_to_datetime(pubdate_str)
    except Exception:
        return datetime.now()


def scrape_vneconomy() -> pd.DataFrame:
    """
    Lấy tin tức chứng khoán từ VnEconomy RSS feed.

    Cách hoạt động:
        1. Gửi GET request đến URL RSS
        2. Parse XML bằng BeautifulSoup với parser 'xml'
        3. Tìm tất cả thẻ <item> — mỗi item là 1 bài viết
        4. Trích xuất title, link, pubDate, description
        5. Trả về DataFrame

    Returns:
        DataFrame với các cột: title, url, source, published_at, summary
    """
    try:
        response = requests.get(VNECONOMY_RSS, headers=HEADERS, timeout=10)
        response.raise_for_status()

    except requests.RequestException as e:
        print(f"[news] Lỗi request: {e}")
        return pd.DataFrame()

    # Parse XML bằng lxml (cần pip install lxml)
    soup = BeautifulSoup(response.text, "xml")

    # Mỗi <item> trong RSS là 1 bài viết
    items = soup.find_all("item")

    if not items:
        print("[news] Không tìm thấy bài viết nào trong RSS!")
        return pd.DataFrame()

    articles = []
    for item in items:
        try:
            title = (
                item.find("title").get_text(strip=True) if item.find("title") else ""
            )
            url = item.find("link").get_text(strip=True) if item.find("link") else ""

            # pubDate là thời gian đăng bài theo định dạng RFC 2822
            pubdate_tag = item.find("pubDate")
            published_at = (
                parse_pubdate(pubdate_tag.text) if pubdate_tag else datetime.now()
            )

            # description của VnEconomy là plain text, không cần parse HTML
            desc_tag = item.find("description")
            summary = desc_tag.get_text(strip=True) if desc_tag else ""

            articles.append(
                {
                    "title": title,
                    "url": url,
                    "source": "VnEconomy",
                    "published_at": published_at,
                    "summary": summary,
                }
            )

        except Exception as e:
            print(f"[news] Lỗi parse item: {e}")
            continue

    df = pd.DataFrame(articles)

    # Xóa các bài trùng URL
    df = df.drop_duplicates(subset="url")

    print(f"[news] Lấy được {len(df)} bài từ VnEconomy")
    return df


if __name__ == "__main__":
    df = scrape_vneconomy()
    print(df[["title", "published_at", "source"]].head(10))
    print(f"\nCác cột: {df.columns.tolist()}")
    print(f"Tổng số dòng: {len(df)}")
