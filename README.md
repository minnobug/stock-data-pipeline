# 🇻🇳 Vietnam Stock Data Pipeline

An end-to-end ELT pipeline for the Vietnamese stock market (HOSE & HNX), built as a hands-on data engineering project.

## Overview

Collects daily stock prices, company information, and news sentiment from Vietnamese financial sources, transforms and loads them into a Data Warehouse for analysis.

## Tech Stack

- **Containerization:** Docker
- **Data Source:** vnstock, CafeF
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

```bash
git clone https://github.com/minnobug/stock-data-pipeline
cd stock-data-pipeline
docker-compose up -d
```

## Author

**Le Van Minh** — Information Systems 
GitHub: [@minnobug](https://github.com/minnobug)
