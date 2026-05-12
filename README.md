# India Inflation ETL Pipeline

An automated ETL pipeline that tracks India's Consumer Price Index (CPI) from 1957–2025, calculates inflation trends, and flags months where inflation exceeded RBI's 6% tolerance limit.

## 🔴 Problem
Analysts at BFSI and consulting firms manually download, clean, and compile India's monthly CPI data every month — a process taking 2–3 hours of repetitive work with no audit trail.

## ✅ Solution
A fully automated Python ETL pipeline that:
- Auto-downloads latest CPI data from FRED (Federal Reserve Database)
- Cleans and transforms raw data
- Calculates Month-on-Month and Year-on-Year inflation
- Flags high inflation months (YoY > 6% — RBI's upper limit)
- Loads structured data into SQLite database
- Runs automatically every month via GitHub Actions

## 📊 Key Insights (2000–2025)
- 🔴 123 out of 303 months exceeded RBI's 6% inflation limit
- 📈 2010s were the worst decade: avg inflation 7.34%
- 📉 2020s improving: avg inflation 5.04%

## 🏗️ Architecture
FRED API → Extract → Transform → Load → SQLite DB → Power BI Dashboard

## ⚙️ Tech Stack
- Python, Pandas — data processing
- Requests — auto data download
- SQLite — structured storage
- GitHub Actions — monthly automation
- Power BI — visualization

## 💼 Business Impact
| Before | After |
|--------|-------|
| 2–3 hrs manual work monthly | 0 hrs — fully automated |
| Error-prone Excel updates | Validated, logged pipeline |
| No historical view | 68 years of structured data |
| No alerts | Auto-flagging of high inflation months |

## 🚀 How to Run
```bash
git clone https://github.com/shoaib-data/india-inflation-etl-pipeline.git
cd india-inflation-etl-pipeline
pip install -r requirements.txt
python pipeline.py
```

## 📁 Project Structure
├── pipeline.py          # Main ETL pipeline
├── requirements.txt     # Dependencies
├── .github/workflows/   # GitHub Actions automation
├── data/
│   ├── raw/             # Raw downloaded data
│   └── inflation.db     # SQLite database
