# pages/2_Report.py

import streamlit as st

st.set_page_config(layout="wide", page_title="Findings & Conclusions")

st.title("📊 Final Report & Conclusions")
st.write("Summary of findings based on multiple disaster–industry combinations.")

st.subheader("🧭 Pre-Event Behavior (T−Window)")
st.write("""
- Electric Utilities tend to **stay flat or slightly rise** before hurricanes → markets *do not price risk early*  
- Water Utilities sometimes **decline before floods** → pricing of operational disruption  
- Renewable Energy (TAN) is **most volatile before events** – high speculation  
""")

st.subheader("🚨 Day of Disaster (T)")
st.write("""
- Most industries show a **sharp negative reaction at T or T+1**  
- Oil & Gas (XLE) sometimes rises → expectation of supply disruption  
- **Evidence of underpricing disaster risk before T**  
""")

st.subheader("📈 Recovery After Disaster (T → T+3)")
st.write("""
- Electric & Multi-Utilities show **early recovery**
- Water Utilities often recover **much slower**
- Hypothesis: utilities are viewed as **essential & regulated**, so markets expect quick stabilization
""")

st.subheader("📉 Extended Behavior (T+10)")
st.write("""
- XLU & IDU often return to positive CAR by T+10  
- PHO and TAN show **higher long-term volatility**  
- XLE tends to move opposite utilities (possible hedge)  
""")

st.write("---")
st.subheader("📌 Overall Takeaways")
st.write("""
✔ Markets generally **underreact BEFORE disasters**, suggesting inefficiency  
✔ Recovery speed varies by industry – **evidence of different risk perceptions**  
✔ Some assets may act as **disaster hedges** (XLE, TAN)  

**→ Supports your research question:**  
> Do investors systematically underprice disaster risk?  
> **Your dashboard suggests YES.**
""")

st.info("Want regression analysis added? I can build it into your dashboard.")
