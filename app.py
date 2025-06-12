import streamlit as st
from streamlit_option_menu import option_menu

from tabs import (tab0_welcome, tab1_inputs, tab2_constraints,
                  tab3_coefficients, tab4_optimization, tab5_scenarios)
from utils.data_utils import load_slider_data

st.set_page_config("Carbon Portfolio Optimizer", layout="wide")
st.title("Toolkit: CDR Portfolio Optimization")


with st.sidebar:
    selected = option_menu(
        "Navigation",
        options=[
            "Welcome",
            "Resource inputs",
            "Method constraints",
            "Resource coefficients",
            "Portfolio generation",
            "Scenario comparison",
            "Sensitivity analysis",
        ],
        icons=["house", "upload", "gear", "sliders", "graph-up-arrow", "card-checklist", "search"],
        default_index=0,
        orientation="vertical"
    )

# Dispatch to appropriate tab
cost_sliders = load_slider_data()


if selected == "Welcome":
    tab0_welcome.render_tab()
elif selected == "Resource inputs":
    tab1_inputs.render_tab()
elif selected == "Method constraints":
    tab2_constraints.render_tab()
elif selected == "Resource coefficients":
    tab3_coefficients.render_tab(cost_sliders)
elif selected == "Portfolio generation":
    tab4_optimization.render_tab()
elif selected == "Scenario comparison":
    tab5_scenarios.render_tab()
# elif selected == "Sensitivity analysis":
#     tab5_sensitivity.render_tab()
