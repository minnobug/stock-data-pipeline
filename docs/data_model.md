# Data Model — Vietnam Stock Data Pipeline

## Overview

The warehouse schema follows a **Galaxy Schema** design with shared dimension tables across multiple fact tables.

```
raw layer (PostgreSQL public schema)
    ↓ dbt staging
    ↓ dbt marts
warehouse layer (PostgreSQL warehouse schema)
```

---

## Raw Layer (`public` schema)

Data loaded directly from sources — no transformation applied.

### `raw_companies`
| Column | Type | Description |
|--------|------|-------------|
| ticker | VARCHAR(20) PK | Stock symbol (e.g. VNM, VIC) |
| name | VARCHAR(255) | Company name in Vietnamese |
| exchange | VARCHAR(20) | HOSE or HNX |
| industry | VARCHAR(100) | Type: stock, etf, ... |
| is_delisted | BOOLEAN | Whether delisted from exchange |
| updated_at | TIMESTAMP | Last updated timestamp |

### `raw_candles`
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | Auto-increment ID |
| ticker | VARCHAR(20) | Stock symbol |
| trade_date | DATE | Trading date |
| open | NUMERIC(18,2) | Opening price (VND) |
| high | NUMERIC(18,2) | Highest price (VND) |
| low | NUMERIC(18,2) | Lowest price (VND) |
| close | NUMERIC(18,2) | Closing price (VND) |
| volume | BIGINT | Trading volume |
| inserted_at | TIMESTAMP | Record insertion time |

### `raw_news`
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | Auto-increment ID |
| title | TEXT | Article title |
| url | TEXT UNIQUE | Article URL |
| source | VARCHAR(100) | Source name (VnEconomy) |
| published_at | TIMESTAMP | Publication datetime |
| summary | TEXT | Article summary |
| inserted_at | TIMESTAMP | Record insertion time |

---

## Warehouse Layer (`warehouse` schema)

Transformed and modeled data ready for analysis.

### Dimension Tables

#### `dim_companies`
| Column | Type | Description |
|--------|------|-------------|
| company_id | VARCHAR(20) PK | Stock symbol |
| ticker | VARCHAR(20) | Stock symbol |
| name | VARCHAR(255) | Company name |
| exchange | VARCHAR(20) | HOSE or HNX |
| industry | VARCHAR(100) | Industry type |
| is_delisted | BOOLEAN | Delisting status |
| updated_at | TIMESTAMP | Last updated |

#### `dim_times`
| Column | Type | Description |
|--------|------|-------------|
| date_id | DATE PK | Trading date |
| trade_date | DATE | Trading date |
| day_of_week | INT | 0=Sunday ... 6=Saturday |
| day | INT | Day of month |
| month | INT | Month (1-12) |
| quarter | INT | Quarter (1-4) |
| year | INT | Year |
| month_name | TEXT | Month name (e.g. January) |
| day_name | TEXT | Day name (e.g. Monday) |

### Fact Tables

#### `fact_candles`
| Column | Type | Description |
|--------|------|-------------|
| company_id | VARCHAR(20) FK | → dim_companies |
| date_id | DATE FK | → dim_times |
| company_name | VARCHAR(255) | Denormalized company name |
| exchange | VARCHAR(20) | Denormalized exchange |
| industry | VARCHAR(100) | Denormalized industry |
| day_of_week | INT | Denormalized from dim_times |
| day / month / quarter / year | INT | Time breakdown |
| open / high / low / close | NUMERIC | OHLC prices (VND) |
| volume | BIGINT | Trading volume |
| price_change | NUMERIC | close - open |
| price_change_pct | NUMERIC | % change from open to close |

#### `fact_news`
| Column | Type | Description |
|--------|------|-------------|
| news_id | INT PK | Article ID |
| title | TEXT | Article title |
| url | TEXT | Article URL |
| source | VARCHAR(100) | Source name |
| published_at | TIMESTAMP | Publication time |
| summary | TEXT | Article summary |
| day_of_week / day / month / quarter / year | INT | Time breakdown |

---

## Business Requirements Mapping

| Requirement | Tables Used |
|-------------|-------------|
| BR1: Stock price trend analysis | `fact_candles` + `dim_times` |
| BR2: Market sentiment from news | `fact_news` |
| BR3: Trading volume analysis | `fact_candles` |
| BR4: Sector & industry analysis | `fact_candles` + `dim_companies` |

