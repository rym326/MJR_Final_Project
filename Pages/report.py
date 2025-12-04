import streamlit as st

st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 6rem !important;
        }
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def show_report():
    st.title("Event Study Report: Utility Industry Reactions to Major U.S. Natural Disasters")

    st.markdown("""
    ## 1. Introduction
    This report analyzes how U.S. utility-related industries react to major natural disasters using an event-study 
    framework. Instead of examining individual firms, the analysis focuses on sector-level ETFs:

    - Electric Utilities (XLU)  
    - Multi-Utilities (IDU)  
    - Renewable Energy – Solar (TAN)  
    - Water Utilities (PHO)  
    - Oil & Gas (XLE)

    Each ETF’s performance is compared to the market benchmark SPY (S&P 500 ETF) to compute **abnormal returns**—
    movements that cannot be explained by overall market conditions. The goal is to measure how different types of 
    disasters affect industry-specific performance and whether certain sectors behave defensively or cyclically 
    around extreme weather events.

    ---

    ## 2. Calculating Abnormal (Excess) Returns
    Daily percentage returns are computed for each ETF and the benchmark:

    ```python
    returns = close_prices_full.pct_change().dropna()
    benchmark_returns = returns[BENCHMARK]
    abnormal = returns[industry_tickers].sub(benchmark_returns, axis=0)
    ```

    **Abnormal Return = Industry Return – Market Return**

    Interpretation:  
    - Positive abnormal return → industry outperforms the market  
    - Negative abnormal return → underperforms the market  

    These abnormal returns form the basis for cumulative abnormal return (CAR) calculations.

    ---

    ## 3. Constructing the Event Window (T−20 to T+20)
    For each disaster:
    - The event date is converted to a timestamp  
    - Price data around the date is downloaded  
    - The nearest available trading day is located  
    - A standardized **41-day window** is created:

    **T−20, …, T−1, T, T+1, …, T+20**

    Each day in the window is labeled using T-notation:

    ```python
    labels.append("T" if offset == 0 else f"T{offset:+d}")
    ```

    This standardization allows all disasters to be aligned on a common timeline.

    ---

    ## 4. Cumulative Abnormal Returns (CAR)
    CAR aggregates daily abnormal returns:

    ```python
    abnormal_cum = abnormal.cumsum() * 100
    ```

    The *×100* expresses results in percentage-point abnormal performance.

    The data is reshaped for visualization:

    ```python
    ab_df = abnormal_cum.reset_index().rename(columns={"index": "T"})
    ab_df = ab_df.melt("T", var_name="Industry", value_name="CAR")
    ```

    CAR indicates how much an industry has gained or lost **relative to the market** from T−20 up to any point after T.

    ---

    ## 5. Short-Horizon Return Comparisons (T to T+10)
    The dashboard also computes short-horizon price differences without smoothing or interpolation:

    ```python
    pre   = industry_prices.loc["T", ticker]   - industry_prices.loc["T-5", ticker]
    short = industry_prices.loc["T+3", ticker] - industry_prices.loc["T", ticker]
    med   = industry_prices.loc["T+10", ticker] - industry_prices.loc["T", ticker]
    ```

    These reflect:
    - **T−5 → T**: Pre-event drift  
    - **T → T+3**: Immediate reaction  
    - **T → T+10**: Early recovery or continuation  

    Results are shown in a bar chart for each industry.

    ---

    ## 6. Dashboard Interaction Overview
    Users may:
    - Select industries  
    - Select one or multiple disasters  
    - Run a full event-study analysis  

    The dashboard displays:
    - **CAR/CAAR line charts** for T−20 → T+20  
    - **Short-horizon return bars**  
    - **Narrative summaries** for interpretation  

    Each selection regenerates all charts dynamically.

    ---
    """
    )
