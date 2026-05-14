# India Inflation ETL Pipeline

An automated ETL pipeline that tracks India's Consumer Price Index (CPI) from 1957 to present, calculates inflation trends, and flags months where inflation exceeded RBI's 6% upper tolerance limit.

> ⚡ **Last auto-updated:** Every 1st of the month via GitHub Actions

## 🔴 Problem
Analysts at BFSI firms and consulting companies manually download India's monthly CPI data from government sources every month — cleaning messy formats, recalculating MoM/YoY changes in Excel, and compiling reports. This takes **2–3 hours of repetitive work monthly** with no automation, no audit trail, and no early warning system for high inflation periods.

## ✅ Solution
A fully automated Python ETL pipeline that runs on GitHub's servers every 1st of the month — no manual effort required after setup.

**What it does automatically:**
- Downloads latest CPI data directly from FRED (Federal Reserve Economic Database)
- Cleans raw data — handles nulls, standardizes column names, filters relevant date range
- Calculates Month-on-Month % change and Year-on-Year % change
- Flags months where YoY inflation exceeded RBI's 6% upper tolerance limit
- Loads structured data into a SQLite database
- Exports clean CSV for reporting
- Logs every step with timestamps for full audit trail

## 📸 Dashboard Preview

![India Inflation Pulse Dashboard](PowerBI%20Dashboard.png)


## 📊 Key Insights (2000–2025)
| Metric | Value |
|--------|-------|
| Total months analyzed | 303 |
| Months above RBI 6% limit 🔴 | 123 (40%) |
| Average inflation — 2000s | 5.69% |
| Average inflation — 2010s | 7.34% (worst decade) |
| Average inflation — 2020s | 5.04% |

> The 2010s spike aligns with India's food inflation crisis (2009–2014) driven by poor monsoons and global commodity price surges.


## 🏗️ Architecture
FRED API (live data)
↓
EXTRACT — download & load raw CSV
↓
TRANSFORM — clean, calculate MoM/YoY, flag high inflation
↓
LOAD — write to SQLite database (inflation.db)
↓
INSIGHTS — SQL queries for summary statistics
↓
Power BI Dashboard — visual reporting
↓
GitHub Actions — runs full pipeline on 1st of every month

## ⚙️ Tech Stack
- Python, Pandas — data processing
- Requests — auto data download
- SQLite — structured storage
- GitHub Actions — monthly automation
- Power BI — visualization

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core pipeline language |
| Pandas | Data cleaning and transformation |
| Requests | Auto-downloading data from FRED API |
| SQLite | Structured database |
| SQLAlchemy | Database connection layer |
| GitHub Actions | Monthly automation scheduler |
| Power BI | Dashboard and visualization |

## 💼 Business Impact
| Before This Pipeline | After This Pipeline |
|----------------------|---------------------|
| 2–3 hrs manual work every month | 0 hrs — fully automated |
| Error-prone Excel copy-paste | Validated, logged ETL pipeline |
| No historical trend view | 68 years of structured monthly data |
| No inflation alerts | Auto-flagging of RBI limit breaches |
| Data siloed in analyst's laptop | Centralized SQLite database |
| No audit trail | Full timestamped log every run |

## 🤖 Automation — GitHub Actions

This pipeline runs automatically on **the 1st of every month at 9:00 AM UTC** via GitHub Actions. No manual intervention needed.

## 🔮 Future Improvements

- Connect Power BI Service to cloud database (Azure SQL / Supabase) for fully automated dashboard refresh
- Add email alerts when monthly inflation crosses RBI 6% limit
- Expand to WPI (Wholesale Price Index) data for producer inflation tracking


## 🚀 How to Run
```bash
git clone https://github.com/shoaib-data/india-inflation-etl-pipeline.git
cd india-inflation-etl-pipeline
pip install -r requirements.txt
python pipeline.py
```

## 📁 Project Structure
india-inflation-etl-pipeline/
├── pipeline.py                   # Full ETL pipeline
├── requirements.txt              # Python dependencies
├── .gitignore                    # Files excluded from repo
├── .github/
│   └── workflows/
│       └── run_pipeline.yml      # GitHub Actions automation
├── data/
│   ├── raw/
│   │   └── india_cpi_raw.csv     # Auto-downloaded raw data
│   ├── inflation.db              # SQLite database (auto-generated)
│   └── inflation_clean.csv       # Clean CSV for Power BI
└── PowerBI Dashboard.png         # Dashboard screenshot


## 👤 Author

**Shoaib** | IIT Madras BS Data Science Student

Targeting Data & AI roles in Delhi NCR

[![GitHub](https://img.shields.io/badge/GitHub-shoaib--data-black?logo=github)](https://github.com/shoaib-data) [![LinkedIn](https://img.shields.io/badge/LinkedIn-shoaib99-blue?logo=linkedin)](https://www.linkedin.com/in/shoaib99/)
