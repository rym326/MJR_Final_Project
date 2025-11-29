# app.py  --> HOME PAGE

import streamlit as st

st.set_page_config(
    page_title="Natural Disaster Impact Dashboard",
    layout="centered",              # Forces sidebar to stay visible
    initial_sidebar_state="expanded"
)

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

### Navigation
Use the sidebar to access:
1. **Event Study Dashboard** – Run the analysis  
2. **Report & Conclusions** – Summary of findings  

---

### Team Members  
- Ryan McGranahan  
- Graham Johnston  
- Thomas Ross  

Let’s get started → **Go to the Event Study Dashboard in the sidebar.**
""")