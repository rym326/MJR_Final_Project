# app.py

import streamlit as st

st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 6rem !important;
        }
        header {visibility: hidden;}   /* removes Streamlit top bar */
    </style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="Natural Disaster Impact Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Event Study Dashboard", "Methodology", "Analysis"])


# -------------------- HOME PAGE --------------------
if page == "Home":
    st.title("Natural Disaster Impact on U.S. Utility Industries")
    st.write("""
Welcome to our final project dashboard.

This tool explores how different utility-related industries react to major U.S. natural disasters
using an event study methodology.

### What You Can Do:
- Analyze stock reactions before and after disaster events  
- Compare utilities across different industries  
- Study Cumulative Abnormal Returns (CAR)  
- Understand how markets recover after disasters

---

### Navigation  
Use the sidebar to access:
1. Event Study Dashboard – Run the analysis 
2. Methodology – Processes involved in event study
3. Analysis – Summary of findings  

---

### Team Members  
- Ryan McGranahan  
- Graham Johnston  
- Thomas Ross
    """)


# -------------------- EVENT STUDY PAGE --------------------
elif page == "Event Study Dashboard":
    from Pages.event_study import show_event_study
    show_event_study()


# -------------------- REPORT PAGE --------------------
elif page == "Methodology":
    from Pages.report import show_report
    show_report()

# -------------------- Analysis PAGE --------------------
elif page == "Analysis":
    from Pages.analysis import show_analysis
    show_analysis()

