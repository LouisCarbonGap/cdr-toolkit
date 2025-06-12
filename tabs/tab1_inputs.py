import pandas as pd
import streamlit as st

from config.config import resource_groups, resource_order, resource_unit_map
from utils.ui_helpers import format_resource_summary


def render_tab():
    
    # initialization
    if "resource_caps" not in st.session_state:
        st.session_state.resource_caps = {r: 0.0 for r in resource_order}
        
    st.header("Resource inputs")

    st.info("""
    **Objective:**
    
    This section lets you define the **total available quantities of each resource** for the optimization model.
    """)
    
    st.warning("""
    ⚠️ Resources with zero availability will block portfolio feasibility if required by active methods.
               """)

    # user inputs
    st.subheader("Set Available Resources")
    cols = st.columns(3)
    for idx, (group, rlist) in enumerate(resource_groups.items()):
        with cols[idx % 3]:
            unit = resource_unit_map.get(group, "")
            st.markdown(f"**{group} ({unit})**")
            for r in rlist:
                name_clean = r.split(" (")[0]
                cap = st.number_input(
                    label=name_clean,
                    min_value=0.0,
                    value=float(st.session_state.resource_caps.get(r, 0.0)),
                    key=f"cap_{r}"
                )
                st.session_state.resource_caps[r] = cap

    # reset button
    st.divider()
    if st.button("🔄 Reset All Resource Inputs"):
        for r in st.session_state.resource_caps:
            st.session_state.resource_caps[r] = 0.0
        st.success("All resource values reset to 0.")
        st.rerun()

    # summary table
    st.subheader("Summary of Available Resources")
    df_caps = pd.DataFrame.from_dict({
        r: st.session_state.resource_caps[r]
        for r in resource_order if st.session_state.resource_caps.get(r, 0) > 0
    }, orient="index", columns=["Available Amount"]).reindex(resource_order).dropna()

    styled = format_resource_summary(df_caps)
    st.table(styled)
    # st.dataframe(styled, use_container_width=True)
