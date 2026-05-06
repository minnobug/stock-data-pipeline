# 🇻🇳 Vietnam Stock Data Pipeline

An end-to-end ELT pipeline for the Vietnamese stock market (HOSE & HNX), built as a hands-on data engineering project.

## Overview

Collects daily stock prices, company information, and news sentiment from Vietnamese financial sources, transforms and loads them into a Data Warehouse for analysis.

## Architecture

```
vnstock (HOSE · HNX)  ─┐
                        ├─→ Python extract ─→ PostgreSQL (raw) ─→ dbt ─→ warehouse schema
VnEconomy RSS feed    ─┘
                                                    ↑
                                              Docker · .env
                                         Kestra orchestration (planned)
```

→ See [`docs/data_model.md`](docs/data_model.md) for full schema documentation.

## Tech Stack

| Layer | Tool |
|-------|------|
| Containerization | Docker |
| Data Sources | vnstock, VnEconomy RSS |
| Raw Database | PostgreSQL |
| Transformation | dbt |
| Warehouse | PostgreSQL (`warehouse` schema) |
| Orchestration | Kestra (planned) |
| Language | Python, SQL |

## Business Requirements

1. Stock price trend analysis (OHLC)
2. Market sentiment analysis from news
3. Trading volume analysis
4. Sector & industry analysis

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/minnobug/stock-data-pipeline
cd stock-data-pipeline
```

### 2. Create environment file

```bash
cp .env.example .env
# Edit .env and fill in your credentials
```

### 3. Start Docker containers

```bash
docker-compose up -d
```

### 4. Initialize the database schema

> ⚠️ Required every time you recreate the containers.

**Windows (PowerShell):**
```powershell
Get-Content load/schema.sql | docker exec -i stock_postgres psql -U admin -d stock_raw
```

**Mac/Linux:**
```bash
docker exec -i stock_postgres psql -U admin -d stock_raw < load/schema.sql
```

### 5. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the pipeline

```bash
python main.py
```

### 7. Run dbt transformations

```bash
cd stock_transform
dbt run
dbt test
```

### 8. View data in pgAdmin

Open `http://localhost:8080` in your browser and login with your pgAdmin credentials from `.env`.

### 9. View dbt documentation

```bash
cd stock_transform
dbt docs generate
dbt docs serve --port 8081
```

Open `http://localhost:8081` to explore the data lineage graph.

## Project Structure

```
stock-data-pipeline/
├── extract/              # Python extraction scripts
│   ├── companies.py      # Company listing from HOSE & HNX
│   ├── vnstock_ohlc.py   # Daily OHLC prices
│   └── news_scraper.py   # News from VnEconomy RSS
├── load/
│   ├── schema.sql        # Raw layer table definitions
│   └── postgres_loader.py # Load data into PostgreSQL
├── stock_transform/      # dbt project
│   └── models/
│       ├── staging/      # Clean raw data
│       └── marts/        # dim & fact tables
├── docs/
│   └── data_model.md     # Schema documentation
├── main.py               # Pipeline entry point
├── docker-compose.yml
└── requirements.txt
```

## Author

**Le Van Minh** — Information Systems @ FPT University HCM  
GitHub: [@minnobug](https://github.com/minnobug) · LinkedIn: [in/lvm205s](https://linkedin.com/in/lvm205s)