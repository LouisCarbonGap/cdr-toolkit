import pandas as pd
import streamlit as st

from config.config import (method_groups, method_order, resource_groups,
                           resource_order, secondary_resources)
from utils.ui_helpers import (format_efficiency_summary, highlight_differences,
                              smart_format)


def render_tab(cost_sliders):
    # initialization
    if "costs" not in st.session_state:
        st.session_state.costs = {
            m: {r: cost_sliders[m][r]["median"] for r in cost_sliders[m]}
            for m in cost_sliders
        }

    st.header("Resource efficiency coefficients")

    st.info("""
    **Objective:**

    This section lets you adjust the resource usage coefficients for each CDR method to best fit your country conditions.

    - Select a **method group** and a **specific method**
    - Adjust the **resource usage coefficients** (e.g., land, energy) using sliders
    - Optionnally **disable** secondary resources (e.g., water, chemicals) to release the constraint from the model
    - **Reset** a single method or all methods to default values with the reset buttons
    - View a **summary table** of current coefficients to be used in the model
    """)

    st.warning("Blue highlights in the table show coefficients modified from their **default median values**.")

    # select combination
    group_selected = st.selectbox("Group selection:", list(method_groups.keys()))
    method_selected = st.selectbox("Method selection:", method_groups[group_selected])

    # sliders
    with st.expander(f"Manage resources for the {method_selected} method", expanded=True):
        for group_name, rlist in resource_groups.items():
            used = [r for r in rlist if r in cost_sliders[method_selected]]
            if not used:
                continue

            st.markdown(f"### {group_name}")
            for r in used:
                conf = cost_sliders[method_selected][r]
                slider_key = f"{method_selected}_{r}_slider"
                toggle_key = f"{method_selected}_{r}_toggle"
                default_val = conf["median"]
                is_secondary = (method_selected, r) in secondary_resources

                # manage toggles
                if is_secondary and toggle_key not in st.session_state:
                    st.session_state[toggle_key] = True

                enabled = True
                if is_secondary:
                    enabled = st.checkbox(f"Use {r}", key=toggle_key)

                if enabled:
                    current_val = st.session_state.costs[method_selected].get(r, default_val)
                    val = st.slider(
                        r,
                        min_value=conf["min"],
                        max_value=conf["max"],
                        value=current_val,
                        step=0.01 if conf["max"] < 10 else 1.0,
                        format="%.2f" if conf["max"] < 10 else "%.0f",
                        key=slider_key,
                    )
                    st.session_state.costs[method_selected][r] = val
                else:
                    st.session_state.costs[method_selected][r] = 0.0
                    st.markdown(f"**DISABLED** ")

        # reset buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset selected method"):
                for r in cost_sliders[method_selected]:
                    default_val = cost_sliders[method_selected][r]["median"]
                    st.session_state.costs[method_selected][r] = default_val

                    slider_key = f"{method_selected}_{r}_slider"
                    toggle_key = f"{method_selected}_{r}_toggle"

                    if slider_key in st.session_state:
                        del st.session_state[slider_key]
                    if (method_selected, r) in secondary_resources and toggle_key in st.session_state:
                        del st.session_state[toggle_key]

                st.success(f"{method_selected} reset to default values.")
                st.rerun()

        with col2:
            if st.button("🔄 Reset all methods"):
                for m in method_order:
                    for r in cost_sliders.get(m, {}):
                        default_val = cost_sliders[m][r]["median"]
                        st.session_state.costs[m][r] = default_val

                        slider_key = f"{m}_{r}_slider"
                        toggle_key = f"{m}_{r}_toggle"

                        if slider_key in st.session_state:
                            del st.session_state[slider_key]
                        if (m, r) in secondary_resources and toggle_key in st.session_state:
                            del st.session_state[toggle_key]

                st.success("All methods reset to default values.")
                st.rerun()

    # summary table
    st.subheader("Summary table: resource usage coefficients in the model")

    df_default = pd.DataFrame(index=method_order, columns=resource_order)
    for m in method_order:
        for r in resource_order:
            df_default.at[m, r] = cost_sliders.get(m, {}).get(r, {}).get("median", 0.0)
    df_default = df_default.astype(float)

    df_current = pd.DataFrame(index=method_order, columns=resource_order)
    for m in method_order:
        for r in resource_order:
            df_current.at[m, r] = st.session_state.costs.get(m, {}).get(r, 0.0)
    df_current = df_current.astype(float)

    styled = format_efficiency_summary(df_current, df_default)
    st.table(styled)
    