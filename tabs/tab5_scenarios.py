import json

import pandas as pd
import plotly.express as px
import streamlit as st


def render_tab():
    st.header("Scenario Comparison")

    if "scenarios" not in st.session_state:
        st.session_state.scenarios = {}

    # --- Import from file ---
    st.markdown("### 📅 Import scenario from JSON or CSV")
    uploaded_file = st.file_uploader("Upload a scenario file", type=["json", "csv"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".json"):
                imported = json.load(uploaded_file)
            else:
                st.warning("CSV import expects a different structure. JSON is preferred.")
                imported = {}

            if isinstance(imported, dict):
                for k, v in imported.items():
                    if k not in st.session_state.scenarios:
                        st.session_state.scenarios[k] = v
                st.success("Scenarios imported successfully.")
            else:
                st.error("Invalid structure in file.")
        except Exception as e:
            st.error(f"Error loading file: {e}")

    if not st.session_state.scenarios:
        st.info("No scenarios have been saved yet.")
        return

    all_scenarios = st.session_state.scenarios
    scenario_names = list(all_scenarios.keys())

    st.markdown("### ✅ Select scenarios to compare")
    selected = st.multiselect("Select scenarios", scenario_names, default=scenario_names)

    # --- Remove scenarios ---
    for name in selected:
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(f"**{name}**")
        with col2:
            if st.button("❌", key=f"remove_{name}"):
                st.session_state.scenarios.pop(name, None)
                st.rerun()

    if not selected:
        st.warning("Please select at least one scenario to display the comparison.")
        return

    all_methods = set()
    all_resources = set()
    for name in selected:
        result = all_scenarios[name]
        all_methods.update(result.get("allocations", {}).keys())
        all_resources.update(result.get("resources", {}).keys())
    all_methods = sorted(all_methods)
    all_resources = sorted(all_resources)

    comparison_data = []
    method_alloc_df = []
    resource_usage_df = []

    for name in selected:
        result = all_scenarios[name]
        allocations = result.get("allocations", {})
        resources = result.get("resources", {})
        constraints = result.get("constraints", {})

        row = {
            "Scenario": name,
            "CO₂ Captured (tCO₂)": result.get("total_co2", 0),
            "Total Cost (€)": result.get("total_cost", 0),
        }

        for method in all_methods:
            value = allocations.get(method, 0)
            row[f"{method} (tCO₂)"] = value
            method_alloc_df.append({"Scenario": name, "Method": method, "tCO₂": value})

        for resource in all_resources:
            total_used = 0
            for method, amount in allocations.items():
                method_info = constraints.get(method, {})
                resource_coeffs = method_info.get("resources", {}) if isinstance(method_info, dict) else {}
                per_unit = resource_coeffs.get(resource, 0)
                total_used += per_unit * amount
                if per_unit > 0:
                    resource_usage_df.append({
                        "Scenario": name,
                        "Method": method,
                        "Resource": resource,
                        "Used": per_unit * amount
                    })
            row[f"{resource} used"] = total_used

        comparison_data.append(row)

    df = pd.DataFrame(comparison_data)
    numeric_cols = df.select_dtypes(include="number").columns
    st.subheader("📊 Comparison Table")
    st.dataframe(df.style.format({col: "{:,.0f}" for col in numeric_cols}, na_rep="-"), use_container_width=True)

    st.download_button("📄 Download Comparison CSV", df.to_csv(index=False).encode("utf-8"),
                       "scenario_comparison.csv", "text/csv")

    st.subheader("📁 Export Individual Scenarios")
    for name in selected:
        scenario_data = json.dumps(all_scenarios[name], indent=2)
        st.download_button(
            label=f"Export '{name}' as JSON",
            data=scenario_data.encode("utf-8"),
            file_name=f"{name}.json",
            mime="application/json"
        )
        flat_df = pd.DataFrame.from_dict(all_scenarios[name].get("allocations", {}), orient="index", columns=["tCO₂"])
        flat_df.index.name = "Method"
        csv_data = flat_df.reset_index().to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"Export '{name}' as CSV",
            data=csv_data,
            file_name=f"{name}.csv",
            mime="text/csv"
        )

    # --- Plot 1: Method allocations ---
    st.subheader("📈 Method Allocations by Scenario")
    df_alloc = pd.DataFrame(method_alloc_df)
    if not df_alloc.empty:
        fig1 = px.bar(df_alloc, x="Method", y="tCO₂", color="Scenario", barmode="group", title="Method Allocations")
        st.plotly_chart(fig1, use_container_width=True)

    # --- Plot 2: Resource usage per method ---
    st.subheader("📊 Resource Usage per Method and Scenario")
    df_resource = pd.DataFrame(resource_usage_df)
    st.write("DEBUG df_resource columns:", df_resource.columns.tolist())
    st.write("DEBUG df_resource preview:", df_resource.head())

    if not df_resource.empty:
        fig2 = px.bar(df_resource, x="Resource", y="Used", color="Scenario", facet_col="Method", facet_col_wrap=3,
                      title="Resource Use per Method by Scenario")
        st.plotly_chart(fig2, use_container_width=True)

    # --- Plot 3: Total resource usage per scenario (stacked) ---
    st.subheader("📉 Total Resource Usage per Scenario")
    if not df_resource.empty and all(col in df_resource.columns for col in ["Scenario", "Resource", "Used"]):
        total_resource_df = df_resource.groupby(["Scenario", "Resource"])["Used"].sum().reset_index()
        fig3 = px.bar(total_resource_df, x="Scenario", y="Used", color="Resource", barmode="stack",
                      title="Total Resource Use by Scenario")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Resource usage data is incomplete or missing.")
