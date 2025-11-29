# Pages/event_study.py

import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt
import datetime as dt

def show_event_study():

    st.title("Event Study Dashboard")

    # Natural Disaster Events
    disaster_events = {
        "Hurricane Ida (Aug 29, 2021)": "2021-08-29",
        "Hurricane Harvey (Aug 25, 2017)": "2017-08-25",
        "Hurricane Irma (Sep 10, 2017)": "2017-09-10",
        "Texas Winter Storm (Feb 13, 2021)": "2021-02-13",
        "Winter Storm Elliott (Dec 21, 2022)": "2022-12-21",
        "Winter Storm Jonas (Jan 22, 2016)": "2016-01-22",
        "California Wildfires Start (Aug 14, 2020)": "2020-08-14",
        "Camp Fire California (Nov 8, 2018)": "2018-11-08",
        "Dixie Fire California (Jul 13, 2021)": "2021-07-13",
        "Louisiana Flooding (Aug 12, 2016)": "2016-08-12",
        "Midwest Flooding (Mar 14, 2019)": "2019-03-14",
        "Houston Flooding (May 7, 2019)": "2019-05-07",
    }

    # Industry ETFs
    industry_map = {
        "Electric Utilities": "XLU",
        "Multi-Utilities": "IDU",
        "Renewable Energy (Solar)": "TAN",
        "Water Utilities": "PHO",
        "Oil & Gas": "XLE",
    }

    BENCHMARK = "SPY"
    FIXED_WINDOW = 20

    # Sidebar Inputs
    selected_industry = st.sidebar.multiselect(
        "Select industry:",
        options=list(industry_map.keys()),
        default=["Electric Utilities"]
    )

    selected_disaster = st.sidebar.selectbox(
        "Select natural disaster:",
        list(disaster_events.keys())
    )

    normalize = st.sidebar.checkbox("Normalize to 100 at T", value=True)

    if st.sidebar.button("Run Analysis"):

        if not selected_industry:
            st.error("Select at least one industry")
            st.stop()

        event_dt = pd.to_datetime(disaster_events[selected_disaster])
        start_dt = event_dt - dt.timedelta(days=FIXED_WINDOW * 2)
        end_dt = event_dt + dt.timedelta(days=FIXED_WINDOW * 2)

        tickers = [industry_map[i] for i in selected_industry] + [BENCHMARK]
        data = yf.download(tickers, start=start_dt, end=end_dt, progress=False)

        if data.empty:
            st.error("No data found for this event")
            st.stop()

        close_prices = data["Close"].dropna(how="all")

        trading_dates = close_prices.index
        event_index = trading_dates.get_indexer([event_dt], method="nearest")[0]

        start_slice = event_index - FIXED_WINDOW
        end_slice = event_index + FIXED_WINDOW

        if start_slice < 0 or end_slice >= len(trading_dates):
            start_slice = max(0, start_slice)
            end_slice = min(len(trading_dates) - 1, end_slice)

        close_prices = close_prices.iloc[start_slice:end_slice + 1]

        labels = []
        for i in range(len(close_prices.index)):
            offset = i - event_index
            labels.append("T" if offset == 0 else f"T{offset:+d}")

        close_prices.index = labels

        industry_prices = close_prices[[industry_map[i] for i in selected_industry]].copy()

        if normalize:
            industry_prices = (industry_prices / industry_prices.loc["T"]) * 100

        st.subheader("Cumulative Abnormal Returns (CAR)")
        returns = close_prices.pct_change().dropna()
        benchmark_returns = returns[BENCHMARK]
        abnormal = returns[industry_prices.columns].sub(benchmark_returns, axis=0)
        abnormal_cum = abnormal.cumsum() * 100

        plot_df = abnormal_cum.reset_index().rename(columns={"index": "T"})
        plot_df = plot_df.melt("T", var_name="Industry", value_name="CAR")

        chart = (
            alt.Chart(plot_df)
            .mark_line(point=True)
            .encode(
                x=alt.X("T:N", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("CAR:Q", title="Cumulative Abnormal Return (%)"),
                color="Industry:N",
                tooltip=["T", "Industry", "CAR"]
            )
        )
        st.altair_chart(chart, use_container_width=True)
