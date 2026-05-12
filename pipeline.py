import pandas as pd
import sqlite3
import os
import requests
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────
RAW_DATA_PATH = "data/raw/india_cpi_raw.csv"
DB_PATH = "data/inflation.db"
LOG_PATH = "data/pipeline.log"

# ── LOGGER ──────────────────────────────────────────
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(LOG_PATH, "a") as f:
        f.write(full_message + "\n")

# ── DOWNLOAD ────────────────────────────────────────
def download_data():
    log("DOWNLOAD: Fetching latest CPI data from FRED...")
    
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=INDCPIALLMINMEI"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(RAW_DATA_PATH, 'wb') as f:
            f.write(response.content)
        log("DOWNLOAD: File saved successfully to data/raw/india_cpi_raw.csv")
    else:
        log(f"DOWNLOAD: Failed to fetch data. Status code: {response.status_code}")
        raise Exception("Data download failed")

# ── EXTRACT ─────────────────────────────────────────
def extract():
    log("EXTRACT: Starting data extraction...")
    
    df = pd.read_csv(RAW_DATA_PATH)
    
    log(f"EXTRACT: Loaded {len(df)} rows and {len(df.columns)} columns")
    log(f"EXTRACT: Columns found: {list(df.columns)}")
    log(f"EXTRACT: Date range: {df['observation_date'].min()} to {df['observation_date'].max()}")
    df.columns = ['date', 'cpi_value']
    return df

# ── TRANSFORM ───────────────────────────────────────
def transform(df):
    log("TRANSFORM: Starting transformation...")

    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Drop nulls
    before = len(df)
    df = df.dropna()
    after = len(df)
    log(f"TRANSFORM: Dropped {before - after} null rows")

    # Extract year and month
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    # Filter from 2000 onwards — more relevant for modern analysis
    df = df[df['year'] >= 2000]
    log(f"TRANSFORM: Filtered to year 2000+, {len(df)} rows remaining")

    # Calculate Month-on-Month % change
    df = df.sort_values('date').reset_index(drop=True)
    df['mom_change'] = df['cpi_value'].pct_change() * 100
    df['mom_change'] = df['mom_change'].round(2)

    # Calculate Year-on-Year % change
    df['yoy_change'] = df['cpi_value'].pct_change(periods=12) * 100
    df['yoy_change'] = df['yoy_change'].round(2)

    # Flag high inflation months (YoY > 6% — RBI's upper tolerance limit)
    df['high_inflation_flag'] = df['yoy_change'] > 6

    log(f"TRANSFORM: High inflation months flagged: {df['high_inflation_flag'].sum()}")
    log("TRANSFORM: Transformation complete")

    return df

# ── LOAD ────────────────────────────────────────────
def load(df):
    log("LOAD: Starting data load...")

    conn = sqlite3.connect(DB_PATH)

    df.to_sql('cpi_data', conn, if_exists='replace', index=False)

    log(f"LOAD: {len(df)} rows loaded into table 'cpi_data' in {DB_PATH}")

    # Verify load
    result = pd.read_sql("SELECT COUNT(*) as total_rows FROM cpi_data", conn)
    log(f"LOAD: Verification — {result['total_rows'][0]} rows in database")

    conn.close()
    log("LOAD: Database connection closed")

# ── INSIGHTS ────────────────────────────────────────
def show_insights(df):
    log("INSIGHTS: Generating summary insights...")

    conn = sqlite3.connect(DB_PATH)

    print("\n========== INDIA INFLATION INSIGHTS ==========")

    # 1. Average YoY inflation overall
    avg = pd.read_sql("SELECT ROUND(AVG(yoy_change), 2) as avg_inflation FROM cpi_data WHERE yoy_change IS NOT NULL", conn)
    print(f"\nAverage YoY Inflation (2000-2025): {avg['avg_inflation'][0]}%")

    # 2. Highest inflation month
    highest = pd.read_sql("SELECT date, ROUND(yoy_change, 2) as yoy_change FROM cpi_data ORDER BY yoy_change DESC LIMIT 1", conn)
    print(f"Highest Inflation Month: {highest['date'][0]} at {highest['yoy_change'][0]}%")

    # 3. Lowest inflation month
    lowest = pd.read_sql("SELECT date, ROUND(yoy_change, 2) as yoy_change FROM cpi_data WHERE yoy_change IS NOT NULL ORDER BY yoy_change ASC LIMIT 1", conn)
    print(f"Lowest Inflation Month: {lowest['date'][0]} at {lowest['yoy_change'][0]}%")

    # 4. High inflation months count
    high = pd.read_sql("SELECT COUNT(*) as count FROM cpi_data WHERE high_inflation_flag = 1", conn)
    print(f"Months above RBI 6% limit: {high['count'][0]} out of 303")

    # 5. Avg inflation by decade
    print("\nAverage Inflation by Decade:")
    decade = pd.read_sql("""
        SELECT 
            (year/10)*10 as decade,
            ROUND(AVG(yoy_change), 2) as avg_inflation
        FROM cpi_data
        WHERE yoy_change IS NOT NULL
        GROUP BY decade
        ORDER BY decade
    """, conn)
    print(decade.to_string(index=False))

    conn.close()
    print("\n==============================================")

# ── MAIN ────────────────────────────────────────────
if __name__ == "__main__":
    log("========== PIPELINE STARTED ==========")
    download_data()
    raw_df = extract()
    transformed_df = transform(raw_df)
    load(transformed_df)
    show_insights(transformed_df)
    log("========== PIPELINE COMPLETE ==========")