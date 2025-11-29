import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt
import altair as alt

st.set_page_config(layout="wide")

# --------------------------------------------------------------
# NATURAL DISASTERS + DATES  
# (with emojis instead of confirm dropdown hack)
# --------------------------------------------------------------
disaster_events = {
    # Hurricanes
    "Hurricane Ida (Aug 29, 2021)": "2021-08-29",
    "Hurricane Harvey (Aug 25, 2017)": "2017-08-25",
    "Hurricane Irma (Sep 10, 2017)": "2017-09-10",

    # ❄ Winter Storms
    "Texas Winter Storm (Feb 13, 2021)": "2021-02-13",
    "Winter Storm Elliott (Dec 21, 2022)": "2022-12-21",
    "Winter Storm Jonas (Jan 22, 2016)": "2016-01-22",

    # Wildfires
    "California Wildfires Start (Aug 14, 2020)": "2020-08-14",
    "Camp Fire California (Nov 8, 2018)": "2018-11-08",
    "Dixie Fire California (Jul 13, 2021)": "2021-07-13",

    # Floods
    "Louisiana Flooding (Aug 12, 2016)": "2016-08-12",
    "Midwest Flooding (Mar 14, 2019)": "2019-03-14",
    "Houston Flooding (May 7, 2019)": "2019-05-07",
}

# --------------------------------------------------------------
# INDUSTRIES (ETF REPRESENTATIVES)
# --------------------------------------------------------------
industry_map = {
    "Electric Utilities": "XLU",
    "Multi-Utilities": "IDU",
    "Renewable Energy (Solar)": "TAN",
    "Water Utilities": "PHO",
    "Oil & Gas": "XLE",
}

BENCHMARK = "SPY"
FIXED_WINDOW = 20     # Fixed: T-20 to T+20

# --------------------------------------------------------------
# HOME PAGE
# --------------------------------------------------------------
if mode == "event_study":
    st.title("Natural Disaster Impact on U.S. Utility Industries")
    st.write("""
        This dashboard explores **how different utility-related industries reacted to major U.S. natural disasters**.
        Select a disaster + industry to analyze returns around the event date.
    """)
    st.write("---")

    # ------------------- INDUSTRY SELECT -------------------
    selected_industry = st.sidebar.multiselect(
        "Which industry do you want to visualize?",
        options=list(industry_map.keys()),
        default=["Electric Utilities"],
    )

    # ------------------- SINGLE STREAMLIT DROPDOWN (NO CONFIRMATION) -------------------
    selected_disaster = st.sidebar.selectbox(
        "Select a Natural Disaster",
        list(disaster_events.keys())
    )

    window = FIXED_WINDOW
    st.sidebar.write(f"Event window: **T-{window} to T+{window}** (fixed)")
    normalize = st.sidebar.checkbox("Normalize to 100 at T", value=True)

# ------------------- RUN ANALYSIS -------------------
if st.sidebar.button("Run Analysis"):

    if not selected_industry:
        st.error("Please select at least one industry.")
        st.stop()

    st.subheader(f"**{selected_disaster}**")

    # Convert event date
    event_dt = pd.to_datetime(disaster_events[selected_disaster])

    # 🔥 Request MUCH larger window so we guarantee enough trading days
    start_dt = event_dt - dt.timedelta(days=FIXED_WINDOW * 2)   # 20 x 2 = 40 days before
    end_dt = event_dt + dt.timedelta(days=FIXED_WINDOW * 2)     # 40 days after

    # Tickers to fetch
    industry_tickers = [industry_map[i] for i in selected_industry]
    all_tickers = list(set(industry_tickers + [BENCHMARK]))

    # Download data
    data = yf.download(all_tickers, start=start_dt, end=end_dt, progress=False)

    if data.empty:
        st.error("⚠ No data available for this event. Try another industry or disaster.")
        st.stop()

    # Use closing prices only
    close_prices_full = data["Close"].dropna(how="all")

    # -------------------------
    # FORCE EXACT T-10 → T+10 TRADING WINDOW
    # -------------------------

    trading_dates = close_prices_full.index
    event_index = trading_dates.get_indexer([event_dt], method="nearest")[0]

    # Desired index range around the event
    start_slice = event_index - FIXED_WINDOW
    end_slice   = event_index + FIXED_WINDOW

    # CHECK if enough data exists — if not, warn user
    if start_slice < 0 or end_slice >= len(trading_dates):
        st.warning(
            f"⚠ Only {event_index} trading days available before T — showing available range."
        )
        start_slice = max(0, start_slice)
        end_slice   = min(len(trading_dates) - 1, end_slice)

    # Apply final slice
    close_prices_full = close_prices_full.iloc[start_slice:end_slice + 1]

    # OPTIONAL — Show user what window they actually got
    first_label = close_prices_full.index[0]
    last_label = close_prices_full.index[-1]

    # ------------------- T-LABELING -------------------
    trading_dates = close_prices_full.index
    event_index = trading_dates.get_indexer([event_dt], method="nearest")[0]

    labels = []
    for i in range(len(trading_dates)):
        offset = i - event_index
        labels.append("T" if offset == 0 else f"T{offset:+d}")

    close_prices_full.index = labels
    industry_prices = close_prices_full[industry_tickers].copy()

    if normalize:
        industry_prices = (industry_prices / industry_prices.loc["T"]) * 100

    # ------------------- CAR -------------------
    st.subheader("Cumulative Abnormal Returns (CAR)")
    returns = close_prices_full.pct_change().dropna()
    benchmark_returns = returns[BENCHMARK]
    abnormal = returns[industry_tickers].sub(benchmark_returns, axis=0)
    abnormal_cum = abnormal.cumsum() * 100

    ab_df = abnormal_cum.reset_index().rename(columns={"index": "T"})
    ab_df = ab_df.melt("T", var_name="Industry", value_name="CAR")

    CAR_chart = (
        alt.Chart(ab_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("T:N", sort=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("CAR:Q", title="Cumulative Abnormal Return (%)"),
            color="Industry:N",
            tooltip=["T", "Industry", "CAR"]
        )
    )
    st.altair_chart(CAR_chart, use_container_width=True)

    # ------------------- POST-EVENT BARS -------------------
    st.subheader("Post-Event Performance")
    labels_needed = ["T-5", "T", "T+3", "T+10"]
    missing = [lbl for lbl in labels_needed if lbl not in industry_prices.index]

    if missing:
        st.warning(f"Not enough data: {', '.join(missing)}")
    else:
        for industry in selected_industry:
            ticker = industry_map[industry]
            pre = industry_prices.loc["T", ticker] - industry_prices.loc["T-5", ticker]
            short = industry_prices.loc["T+3", ticker] - industry_prices.loc["T", ticker]
            med = industry_prices.loc["T+10", ticker] - industry_prices.loc["T", ticker]

            perf_df = pd.DataFrame({
                "Period": ["T-5 → T", "T → T+3", "T → T+10"],
                "Return (%)": [pre, short, med]
            })
            perf_df["Color"] = perf_df["Return (%)"].apply(lambda x: "green" if x >= 0 else "red")

            st.write(f"### {industry}")
            bar_chart = (
                alt.Chart(perf_df)
                .mark_bar()
                .encode(
                    x=alt.X("Period:N", sort=["T-5 → T", "T → T+3", "T → T+10"]),
                    y="Return (%):Q",
                    color=alt.Color("Color:N", scale=None),
                    tooltip=["Period", "Return (%)"]
                )
            )
            st.altair_chart(bar_chart, use_container_width=True)