import json

import streamlit as st


@st.cache_data
def load_slider_data():
    """Load slider data from a JSON file and cache it for performance."""
    with open("data/cost_sliders.json") as f:
        return json.load(f)