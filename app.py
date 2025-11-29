import streamlit as st

st.set_page_config(
    page_title="Natural Disaster Impact Dashboard",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Home", "Event Study Dashboard", "Report"]
)

# ---------------- HOME PAGE ----------------
if page == "Home":
    st.title("Natural Disaster Impact on U.S. Utility Industries")
    st.write("""
    Welcome to our final project dashboard!

    This tool explores **how different utility-related industries react to major U.S. natural disasters**
    using an **event study** methodology.

    ### What You Can Do:
    - Analyze stock reactions **before and after** disaster events  
    - Compare utilities across **different industries**  
    - Study **Cumulative Abnormal Returns (CAR)**  
    - Understand **how markets recover after disasters**

    ---
    ### Team Members  
    - Ryan McGranahan  
    - Graham Johnston  
    - Thomas Ross  
    """)

# ---------------- EVENT STUDY PAGE ----------------
elif page == "Event Study Dashboard":
    import event_study  # runs event_study.py automatically

# ---------------- REPORT PAGE ----------------
elif page == "Report":
    import report
