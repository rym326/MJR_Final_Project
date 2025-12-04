# Natural Disaster Event Study: Utility and Energy Industry Reactions

This repository contains the full workflow and Streamlit dashboard used to analyze how major U.S. natural disasters affect the stock performance of utility and energy industries. The project examines four utility-related ETFs (XLU, IDU, TAN, PHO) and the Oil & Gas sector (XLE), comparing each to the S&P 500 benchmark (SPY) using a standardized T–20 to T+20 event-study framework.

---

## Project Links

**Live Streamlit Website**  
https://natural-disaster-event-study.streamlit.app

**GitHub Repository**  
https://github.com/rym326/MJR_Final_Project

---

## Repository Structure

```
MJR_Final_Project/
│
├── app.py                     # Main Streamlit app and navigation
├── requirements.txt           # Dependencies
│
├── Pages/
│   ├── event_study.py         # Data scraping, returns, CAR, event window
│   ├── methodology.py         # Data sources + methodology explanation
│   ├── analysis.py            # Results by disaster category
│   └── report.py              # Written conclusions and takeaways
│
├── images/                    # Exported figures for presentation
│   ├── Hurricane.png
│   ├── Wildfire.png
│   ├── Winterstorm.png
│   └── Flood.png
│
└── Presentation/
    └── Final_Presentation.pdf
```

---

## Data Sources

**Historical Financial Data (scraped automatically)**  
Downloaded with `yfinance` for: XLU, IDU, TAN, PHO, XLE, SPY  
Source: https://finance.yahoo.com

**Natural Disaster Dates**  
NOAA Storm Events Database  
https://www.ncdc.noaa.gov/stormevents/

---

## Code Overview

### 1. Data Downloading and Preparation  
Location: `Pages/event_study.py`  
Includes:
- Price scraping via `yfinance`
- Daily return and abnormal return calculations
- Construction of the T–20 to T+20 event window
- CAR calculations and formatting for plots
- Interval-based return metrics (T−5→T, T→T+3, T→T+10)

### 2. Analysis  
Location: `Pages/analysis.py`  
Includes structured summaries for:
- Hurricanes  
- Winter storms  
- Wildfires  
- Flooding  
Each with CAR interpretation and sector-level insights.

### 3. Methodology  
Location: `Pages/methodology.py`  
Describes:
- Data pipeline
- Scientific structure of the event study
- Return and CAR definitions
- Explanation of benchmark adjustments

### 4. Written Report  
Location: `Pages/report.py`  
Contains:
- Findings
- Conclusions
- Key takeaways

---

## Presentation Materials

Final class presentation slides:  
`Presentation/Final_Presentation.pdf`

Supporting charts used in the slides:  
`/images/`

---

## Reproducibility Instructions

To rerun the entire project:

```
git clone https://github.com/rym326/MJR_Final_Project.git
pip install -r requirements.txt
streamlit run app.py
```

Running the app recreates all analyses from scratch, including returns, CAR, and visualizations.

---

## Team Members

Ryan McGranahan  
Graham Johnston  
Thomas Ross
