import streamlit as st


def render_tab():
    st.header("Welcome!")
    st.markdown("""
    This tool helps you optimize your carbon direct removal portfolio by adjusting resource usage and constraints.
    
    **Required:**
    1. **Resource inputs**: provide the total available quantities of resources.
    
    **Optionnal:**
    
    2. **Method constraints**: select which carbon removal methods are active and set their maximum portfolio share.
    3. **Resource efficiency coefficients**: adjust the resource usage for each method.
    
    **Outputs:**
    
    4. **Portfolio generation**: run the optimization to find the best portfolio.
    
    **Explore:**
    
    5. **Scenario comparison**: compare different scenarios based on the optimization results.
    6. **Sensitivity analysis**: analyze how changes in method shares or resource availability affect the portfolio.
    
    Let's get started! Use the side tabs to navigate through the sections.
    """)
