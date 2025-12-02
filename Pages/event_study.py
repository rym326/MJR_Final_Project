import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import altair as alt

# --------------------------------------------------------------
# GLOBAL STYLING (tightens top padding, hides default header)
# --------------------------------------------------------------
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 6rem !important;
        }
        header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------
# NATURAL DISASTERS + DATES
# --------------------------------------------------------------
disaster_events = {
    # Hurricanes
    "Hurricane Ida (Aug 29, 2021)": "2021-08-29",
    "Hurricane Harvey (Aug 25, 2017)": "2017-08-25",
    "Hurricane Irma (Sep 10, 2017)": "2017-09-10",
    # Winter Storms
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
FIXED_WINDOW = 20  # T-20 to T+20
T_VALUES = list(range(-FIXED_WINDOW, FIXED_WINDOW + 1))  # [-20, ..., +20]


def _fetch_event_car(event_label, tickers):
    """
    For a single event:
      - download data
      - cut to T-20..T+20 around event
      - compute CAR for each ticker vs benchmark
    Returns:
      DataFrame with index = t (-20..+20), columns = tickers
      or None if data is unusable.
    """
    event_date = pd.to_datetime(disaster_events[event_label])

    # Wider calendar window to guarantee enough trading days
    start_dt = event_date - dt.timedelta(days=FIXED_WINDOW * 2)
    end_dt = event_date + dt.timedelta(days=FIXED_WINDOW * 2)

    data = yf.download(tickers, start=start_dt, end=end_dt, progress=False)
    if data.empty:
        return None

    close_prices = data["Close"].dropna(how="all")
    trading_dates = close_prices.index

    # Nearest trading day to the event date
    event_index = trading_dates.get_indexer([event_date], method="nearest")[0]

    start_slice = event_index - FIXED_WINDOW
    end_slice = event_index + FIXED_WINDOW

    # Require full window – otherwise skip this event
    if start_slice < 0 or end_slice >= len(trading_dates):
        return None

    window_prices = close_prices.iloc[start_slice : end_slice + 1].copy()
    window_prices.index = T_VALUES  # numeric t = -20..+20

    # Returns, abnormal returns, CAR
    returns = window_prices.pct_change().fillna(0.0)
    benchmark_returns = returns[BENCHMARK]
    abnormal = returns[tickers].sub(benchmark_returns, axis=0)
    abnormal_cum = abnormal.cumsum() * 100  # percent

    # index is numeric t
    return abnormal_cum


def _event_time_axis():
    """
    Build a nice axis: ticks at t = -20..+20, labels like T-20, T, T+1, etc.
    """
    return alt.Axis(
        values=T_VALUES,
        labelExpr=(
            "datum.value === 0 ? 'T' : "
            "datum.value < 0 ? 'T' + datum.value : 'T+' + datum.value"
        ),
        title="",  # no big 'T' under axis
    )


# --------------------------------------------------------------
# MAIN PAGE FUNCTION
# --------------------------------------------------------------
def show_event_study():
    st.title("Natural Disaster Impact on U.S. Utility Industries")
    st.write(
        """
        This dashboard explores how different utility-related industries reacted to major U.S. natural disasters
        using an event study methodology.

        You can now select multiple disasters and view the average **Cumulative Abnormal Return (CAAR)**
        across those events, or overlay each event's **CAR** separately.
        """
    )
    st.write("---")

    # ---------- SIDEBAR CONTROLS ----------
    selected_industries = st.sidebar.multiselect(
        "Select Industries:",
        options=list(industry_map.keys()),
        default=["Electric Utilities"],
    )

    selected_disasters = st.sidebar.multiselect(
        "Select One or More Natural Disasters:",
        options=list(disaster_events.keys()),
        default=["Hurricane Ida (Aug 29, 2021)"],
    )

    if not selected_industries:
        st.sidebar.warning("Select at least one industry.")
    if not selected_disasters:
        st.sidebar.warning("Select at least one disaster.")

    chart_mode = st.sidebar.radio(
        "How do you want to visualize the events?",
        ["Average across events (CAAR)", "Show each event separately (CAR)"],
        index=0,
    )

    st.sidebar.write(f"Event window: **T-{FIXED_WINDOW} to T+{FIXED_WINDOW}**")

    if not (selected_industries and selected_disasters):
        return

    if not st.sidebar.button("Run Analysis"):
        return

    # ---------- PREP COMMON OBJECTS ----------
    industry_tickers = [industry_map[i] for i in selected_industries]
    ticker_to_industry = {v: k for k, v in industry_map.items()}
    all_tickers = list(set(industry_tickers + [BENCHMARK]))

    # ---------- LOOP OVER EVENTS, COLLECT CAR ----------
    event_car_dict = {}
    skipped = []

    for event_label in selected_disasters:
        abnormal_cum = _fetch_event_car(event_label, all_tickers)
        if abnormal_cum is None:
            skipped.append(event_label)
            continue
        event_car_dict[event_label] = abnormal_cum[industry_tickers]  # keep only industries

    if skipped:
        st.warning(
            "The following events were skipped due to insufficient or missing data:\n- "
            + "\n- ".join(skipped)
        )

    if not event_car_dict:
        st.error("No usable events after filtering. Try different selections.")
        return

    # =====================================================================
    # CHART 1: CAAR OR MULTI-EVENT CAR (x = numeric t)
    # =====================================================================

    x_scale = alt.Scale(domain=[-FIXED_WINDOW, FIXED_WINDOW])

    if chart_mode == "Average across events (CAAR)":
        st.subheader(
            f"Average Cumulative Abnormal Return (CAAR) across {len(event_car_dict)} event(s)"
        )

        # Stack [events, T-window, industries] and average over events
        stacked = np.stack([df.values for df in event_car_dict.values()], axis=0)
        mean_vals = np.nanmean(stacked, axis=0)  # shape (41, num_industries)

        caar_wide = pd.DataFrame(mean_vals, index=T_VALUES, columns=industry_tickers)

        # Long format
        caar_long = (
            caar_wide.reset_index()
            .rename(columns={"index": "t"})
            .melt("t", var_name="Ticker", value_name="CAR")
        )
        caar_long["Industry"] = caar_long["Ticker"].map(ticker_to_industry)

        # Red vertical line at t = 0
        event_rule = alt.Chart(pd.DataFrame({"t": [0]})).mark_rule(
            color="red", strokeDash=[4, 4], strokeWidth=2
        ).encode(x=alt.X("t:Q", scale=x_scale))

        caar_chart = (
            alt.Chart(caar_long)
            .mark_line(point=True)
            .encode(
                x=alt.X("t:Q", scale=x_scale, axis=_event_time_axis()),
                y=alt.Y("CAR:Q", title="Average Cumulative Abnormal Return (%)"),
                color=alt.Color("Industry:N", title="Industry"),
                tooltip=["t", "Industry", "CAR"],
            )
        )

        st.altair_chart(caar_chart + event_rule, use_container_width=True)

        base_for_intervals = caar_wide

    else:
        st.subheader(
            f"Cumulative Abnormal Returns (CAR) for {len(event_car_dict)} event(s)"
        )

        # Long dataframe: (t, Industry, Event)
        long_rows = []
        for event_label, df in event_car_dict.items():
            temp = (
                df.reset_index()
                .rename(columns={"index": "t"})
                .melt("t", var_name="Ticker", value_name="CAR")
            )
            temp["Industry"] = temp["Ticker"].map(ticker_to_industry)
            temp["Event"] = event_label
            long_rows.append(temp)

        all_events_long = pd.concat(long_rows, ignore_index=True)

        event_rule = alt.Chart(pd.DataFrame({"t": [0]})).mark_rule(
            color="red", strokeDash=[4, 4], strokeWidth=2
        ).encode(x=alt.X("t:Q", scale=x_scale))

        car_chart = (
            alt.Chart(all_events_long)
            .mark_line(point=True)
            .encode(
                x=alt.X("t:Q", scale=x_scale, axis=_event_time_axis()),
                y=alt.Y("CAR:Q", title="Cumulative Abnormal Return (%)"),
                color=alt.Color("Industry:N", title="Industry"),
                strokeDash=alt.StrokeDash(
                    "Event:N", legend=alt.Legend(title="Event")
                ),
                tooltip=["t", "Industry", "Event", "CAR"],
            )
        )

        st.altair_chart(car_chart + event_rule, use_container_width=True)

        # For the interval bars, still use the average across events
        stacked = np.stack([df.values for df in event_car_dict.values()], axis=0)
        mean_vals = np.nanmean(stacked, axis=0)
        base_for_intervals = pd.DataFrame(mean_vals, index=T_VALUES, columns=industry_tickers)

    # =====================================================================
    # CHART 2: INTERVAL SUMMARY BARS (BASED ON AVERAGE CAR INSIDE WINDOWS)
    # =====================================================================
    st.subheader("Average CAR Across Key Windows")

    # Window definitions for "Option B"
    interval_windows = {
        "T-5 → T": list(range(-5, 1)),        # -5, -4, -3, -2, -1, 0
        "T → T+3": list(range(0, 4)),         # 0, 1, 2, 3
        "T → T+10": list(range(0, 11)),       # 0 → 10
    }


    for industry_name in selected_industries:
        ticker = industry_map[industry_name]

        # FIXED — use the index from base_for_intervals
        series = base_for_intervals[ticker].reindex(base_for_intervals.index)

        rows = []
        for label, window_points in interval_windows.items():

            # Ensure all points exist
            if not all(pt in series.index.tolist() for pt in window_points):
                st.warning(f"Not enough data for interval '{label}' for {industry_name}.")
                continue

            avg_val = series.loc[window_points].mean()
            rows.append([label, avg_val])

        if not rows:
            continue

        perf_df = pd.DataFrame(rows, columns=["Period", "Average CAR (%)"])
        perf_df["Color"] = perf_df["Average CAR (%)"].apply(
            lambda x: "green" if x >= 0 else "red"
        )

        st.write(f"### {industry_name}")

        bar_chart = (
            alt.Chart(perf_df)
            .mark_bar()
            .encode(
                x=alt.X(
                    "Period:N",
                    sort=["T-5 → T", "T → T+3", "T → T+10"],
                    title="Window",
                ),
                y=alt.Y("Average CAR (%):Q", title="Average CAR (percentage points)"),
                color=alt.Color("Color:N", scale=None, legend=None),
                tooltip=["Period", "Average CAR (%)"],
            )
        )

        st.altair_chart(bar_chart, use_container_width=True)


