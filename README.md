# 🇻🇳 Vietnam Stock Data Pipeline

An end-to-end ELT pipeline for the Vietnamese stock market (HOSE & HNX), built as a hands-on data engineering project.

## Overview

Collects daily stock prices, company information, and news sentiment from Vietnamese financial sources, transforms and loads them into a Data Warehouse for analysis.

## Tech Stack

- **Containerization:** Docker
- **Data Source:** vnstock, VnEconomy
- **Database:** PostgreSQL
- **Data Warehouse:** DuckDB
- **Orchestration:** Kestra
- **Transformation:** dbt
- **Language:** Python, SQL

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

### 7. View data in pgAdmin

Open `http://localhost:8080` in your browser and login with your pgAdmin credentials from `.env`.

## Author

**Le Van Minh** — Information Systems @ FPT University HCM  
GitHub: [@minnobug](https://github.com/minnobug) · LinkedIn: [in/lvm205s](https://linkedin.com/in/lvm205s)