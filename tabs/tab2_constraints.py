# tabs/tab2_constraints.py

import pandas as pd
import streamlit as st

from config.config import method_groups, method_order
from utils.ui_helpers import format_method_summary


def render_tab():
    # initialization-
    if "constraints" not in st.session_state:
        st.session_state.constraints = {
            m: {"active": True, "max_share": 1.0} for m in method_order
        }

    st.header("Method constraints")

    st.info("""
    **Objective:**

    This section lets you control which CDR methods are included in the optimization
    and assign their **maximum portfolio share**.

    - Activate or deactivate individual methods  
    - Set each method's **max share** (as % of the total portfolio)
    """)

    # activation panel
    with st.expander("⚙️ Manage methods (Open/Close)", expanded=False):
        st.subheader("Activate/deactivate methods and set max allocation")

        for group, method_list in method_groups.items():
            st.markdown(f"#### {group}")
            cols = st.columns(4)
            for i, m in enumerate(method_list):
                with cols[i % 4]:
                    toggle_key = f"toggle_{m}"
                    slider_key = f"slider_{m}"

                    current_active = st.session_state.constraints[m]["active"]
                    is_active = st.toggle(m, value=current_active, key=toggle_key)

                    if is_active and not current_active:
                        st.session_state.constraints[m] = {"active": True, "max_share": 1.0}
                    elif not is_active:
                        st.session_state.constraints[m]["active"] = False
                        st.session_state.constraints[m]["max_share"] = 0.0

                    if st.session_state.constraints[m]["active"]:
                        max_share = st.slider(
                            "Max share (%)",
                            min_value=0,
                            max_value=100,
                            value=int(st.session_state.constraints[m]["max_share"] * 100),
                            step=5,
                            key=slider_key
                        )
                        st.session_state.constraints[m]["max_share"] = max_share / 100
                        if max_share == 0:
                            st.warning("Max share is 0% but method is active", icon="⚠️")

    # reset button
    st.divider()
    if st.button("🔄 Reset All Method Constraints"):
        for m in method_order:
            st.session_state.constraints[m] = {"active": True, "max_share": 1.0}
        st.success("All method constraints reset to default.")
        st.rerun()

    # summary table
    st.subheader("Summary table: Active methods in the model")

    active_methods_summary = {
        m: int(st.session_state.constraints[m]["max_share"] * 100)
        for m in method_order if st.session_state.constraints[m]["active"]
    }

    if active_methods_summary:
        df_methods = pd.DataFrame.from_dict(
            active_methods_summary, orient="index", columns=["Max allocation (%)"]
        ).reindex(method_order).dropna()
        df_methods["Max allocation (%)"] = df_methods["Max allocation (%)"].astype(int)

        styled = format_method_summary(df_methods)
        st.table(styled)

    else:
        st.warning("No active methods selected.")
