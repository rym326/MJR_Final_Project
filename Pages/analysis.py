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


def show_analysis():
    st.title("Disaster-Specific Results & Analysis")

    st.markdown("## Hurricanes")
    st.markdown("""
    **Summary of Results**
    - Electric Utilities, Multi-Utilities, and Water Utilities remain stable or slightly positive.  
    - Solar shows a sharp decline from T−10 to T+12 before a strong rebound toward T+20.  
    - Oil & Gas trends downward before T, stabilizes near T, and stays negative through T+20.  

    **Interpretation:**  
    Hurricanes generate the strongest volatility for Solar and Oil & Gas, while regulated utilities remain resilient.
    """)

    st.image("Pages/images/Hurricane.png")  # Replace or delete as needed
    st.markdown("---")

    # ----------------------------------------------------------------------

    st.markdown("## Winter Storms")
    st.markdown("""
    **Summary of Results**
    - Solar suffers the largest negative CAAR in the dataset, remaining below −10% through T+20.  
    - Oil & Gas declines sharply before T but rebounds strongly afterward, finishing positive.  
    - Traditional utilities show mild, persistent negative CAAR with limited recovery.  

    **Interpretation:**  
    Extreme cold exerts broad downward pressure on utilities while creating rebound opportunities for Oil & Gas through increased heating demand.
    """)

    st.image("Pages/images/winterstorm.png")
    st.markdown("---")

    # ----------------------------------------------------------------------

    st.markdown("## Wildfires")
    st.markdown("""
    **Summary of Results**
    - Solar rises strongly before and after T, producing the highest positive CAAR of any disaster–industry pair.  
    - Oil & Gas declines steeply across the window, ending below −10% by T+20.  
    - Electric & Multi-Utilities drift slightly downward but remain contained.  
    - Water Utilities hold near zero.  

    **Interpretation:**  
    Wildfires appear to strengthen renewable-energy sentiment while weakening expectations for fossil fuel firms.
    """)

    st.image("Pages/images/Wildfire.png")
    st.markdown("---")

    # ----------------------------------------------------------------------

    st.markdown("## Flooding")
    st.markdown("""
    **Summary of Results**
    - Electric, Multi-Utilities, and Water Utilities remain nearly flat through the entire T−20 to T+20 window.  
    - Solar experiences a moderate post-event bump.  
    - Oil & Gas declines slightly, but not nearly as sharply as in hurricanes or wildfires.  

    **Interpretation:**  
    Flood-related shocks are either temporary or already priced in, resulting in the smallest abnormal movements across industries.
    """)

    st.image("Pages/images/flood.png")
    st.markdown("---")

    # ----------------------------------------------------------------------

    st.markdown("## Overall Conclusion")
    st.markdown("""
    Traditional utilities exhibit **stable, muted abnormal returns** across all disaster types, reflecting their 
    defensive structure, regulated pricing, and limited exposure to commodity-driven volatility.

    Renewable Energy (Solar) and Oil & Gas demonstrate **the strongest and most disaster-dependent reactions**, shaped by infrastructure sensitivity, reliability concerns, and energy-market expectations.

    There is **no broad market-wide disaster shock** across utilities.  
    Instead, disasters redistribute abnormal returns **between specific industries**, depending on how each type of event affects infrastructure risk and demand patterns.
    """)

    st.markdown("---")

    # ----------------------------------------------------------------------

    st.markdown("## Key Takeaways")
    st.markdown("""
    **1. Utility ETFs act as defensive assets.**  
    Electric Utilities, Multi-Utilities, and Water Utilities show extremely muted abnormal movements.

    **2. Solar and Oil & Gas drive disaster-related abnormal returns.**  
    Their CAAR patterns are steep, persistent, and highly event-specific.

    **3. Disaster type matters more than the disaster itself.**  
    Solar reacts positively to wildfires but sharply negatively to winter storms.

    **4. No uniform negative market reaction exists.**  
    Many industries remain flat or slightly positive even during large disasters.

    **5. Oil & Gas reactions follow physical supply–demand dynamics.**  
    Hurricanes and wildfires generate negative performance; winter storms drive rebounds.

    **6. Solar reactions reflect sentiment and policy narratives.**  
    Wildfire and flood events produce positive abnormal Solar performance, potentially signaling expectations of renewable-infrastructure investment.
    """)
