import streamlit as st

st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
        }
        header {visibility: hidden;}   /* removes Streamlit top bar */
    </style>
""", unsafe_allow_html=True)


# Show the report page
def show_report():
    st.title("Final Report & Conclusions")
    st.write("Summary of findings based on multiple disaster–industry combinations.")

    st.subheader("Pre-Event Behavior (T−Window)")
    st.write(
        "- Electric Utilities tend to stay flat or slightly rise before hurricanes → markets do not price risk early\n"
        "- Water Utilities sometimes decline before floods → pricing of operational disruption\n"
        "- Renewable Energy (TAN) is most volatile before events – high speculation\n"
    )

    st.subheader("Day of Disaster (T)")
    st.write(
        "- Most industries show a sharp negative reaction at T or T+1\n"
        "- Oil & Gas (XLE) sometimes rises → expectation of supply disruption\n"
        "- Evidence of underpricing disaster risk before T\n"
    )

    st.subheader("Recovery After Disaster (T → T+3)")
    st.write(
        "- Electric & Multi-Utilities show early recovery\n"
        "- Water Utilities often recover much slower\n"
        "- Hypothesis: utilities are viewed as essential & regulated, so markets expect quick stabilization\n"
    )

    st.subheader("Extended Behavior (T+10)")
    st.write(
        "- XLU & IDU often return to positive CAR by T+10\n"
        "- PHO and TAN show higher long-term volatility\n"
        "- XLE tends to move opposite utilities (possible hedge)\n"
    )

    st.write("---")
    st.subheader("Overall Takeaways")
    st.write(
        "Markets generally underreact BEFORE disasters, suggesting inefficiency\n"
        "Recovery speed varies by industry – evidence of different risk perceptions\n"
        "Some assets may act as disaster hedges (XLE, TAN)\n"
    )
