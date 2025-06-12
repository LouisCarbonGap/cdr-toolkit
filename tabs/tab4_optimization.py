import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config.config import method_order, resource_order
from optimization.optimization import run_optimization
from utils.ui_helpers import format_results_summary


def render_tab():
    st.header("Portfolio generation")
    st.info("""
    **Objective:**

    This section lets you run the optimization tool, and navigate the results.

    - Click on the **Run Optimization** button to start the optimization process
    - Once the optimization is complete, you can view the results displayed below
    - You can **save** the scenario for later comparison in the **Scenario Comparison** tab
    """)

    if "constraints" not in st.session_state or "costs" not in st.session_state or "resource_caps" not in st.session_state:
        st.error("Required session state values are missing. Please complete the previous steps first.")
        return

    if "scenarios" not in st.session_state:
        st.session_state.scenarios = {}

    # --- Run optimization ---
    if st.button("Run Optimization"):
        success, result = run_optimization(
            resource_caps=st.session_state.resource_caps,
            method_constraints=st.session_state.constraints,
            method_costs=st.session_state.costs,
        )

        if success:
            allocations = result["method_usage"]
            total_cost = sum(
                allocations[m] * sum(st.session_state.costs[m].values())
                for m in allocations
            )

            st.session_state.latest_result = {
                "total_co2": result["total_removed"],
                "total_cost": total_cost,
                "allocations": allocations,
                "resources": st.session_state.resource_caps.copy(),
                "constraints": {
                    method: {
                        "resources": st.session_state.costs[method]  # this contains the resource intensity coefficients
                    }
                    for method in allocations
                }
                ,
            }

            st.success(f"✅ Optimization successful: {result['total_removed']:,} tCO₂ removed")

        else:
            st.error("❌ Optimization failed")
            if "message" in result:
                st.error(result["message"])

    # --- Display results if available ---
    if "latest_result" in st.session_state:
        latest = st.session_state.latest_result
        allocations = latest["allocations"]

        # Result table
        df_result = pd.DataFrame.from_dict(allocations, orient="index", columns=["tCO₂ removed"])
        df_result["Share (%)"] = (df_result["tCO₂ removed"] / df_result["tCO₂ removed"].sum() * 100).round(2)
        df_result = df_result.sort_values(by="tCO₂ removed", ascending=False)

        st.subheader("Optimization Summary")
        st.table(format_results_summary(df_result))

        # Sankey Diagram
        st.subheader("Resource contribution to CO₂ removal")

        methods = df_result.index.tolist()
        resource_caps = latest["resources"]
        method_costs = st.session_state.costs
        resources = [r for r in resource_caps if resource_caps[r] > 0]

        resource_labels = [f"{r}<br><span style='font-size:16px;color:#333;'>{resource_caps[r]:,.2f}</span>" for r in resources]
        method_labels = [f"{m}<br><span style='font-size:16px;color:#333;'>{allocations[m]:,} tCO₂</span>" for m in methods]
        labels = resource_labels + method_labels
        colors = ["#7fc97f"] * len(resources) + ["#beaed4"] * len(methods)

        source, target, values, hover_labels = [], [], [], []
        for r_idx, r in enumerate(resources):
            for m_idx, m in enumerate(methods):
                amount = method_costs[m].get(r, 0.0) * allocations[m]
                if amount > 0:
                    source.append(r_idx)
                    target.append(len(resources) + m_idx)
                    values.append(amount)
                    share_of_cap = (amount / resource_caps[r]) * 100 if resource_caps[r] else 0
                    hover_labels.append(
                        f"<Resource: {r}<br>"
                        f"Method: {m}<br>"
                        f"Amount used: {amount:,.2f}<br>"
                        f"Share of {r} cap: {share_of_cap:.2f}%"
                    )

        fig = go.Figure(data=[go.Sankey(
            node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels, color=colors),
            link=dict(source=source, target=target, value=values, hovertemplate=hover_labels, color="#80c3cf")
        )])

        fig.update_layout(
            height=550,
            margin=dict(t=40, l=10, r=10, b=10),
            font=dict(size=14, color="black"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Resource usage plots
        st.markdown("### Additional insights on resource consumption")
        df_abs, df_rel = [], []
        for m, units in allocations.items():
            for r in resource_order:
                usage_per_unit = method_costs[m].get(r, 0)
                total_used = usage_per_unit * int(units)
                if total_used > 0:
                    relative = total_used / resource_caps[r] * 100 if resource_caps[r] > 0 else 0
                    df_abs.append({"Method": m, "Resource": r, "Used": total_used})
                    df_rel.append({"Resource": r, "Method": m, "% Used": relative})

        if df_abs:
            df_abs = pd.DataFrame(df_abs)
            fig1 = px.bar(df_abs, x="Resource", y="Used", color="Method", barmode="group", title="Absolute resource usage")
            st.plotly_chart(fig1, use_container_width=True)

        if df_rel:
            df_rel = pd.DataFrame(df_rel)
            df_rel_grouped = df_rel.groupby("Resource")["% Used"].sum().reset_index()
            fig2 = px.bar(df_rel_grouped, x="Resource", y="% Used", title="Proportion of total available resources consumed")
            st.plotly_chart(fig2, use_container_width=True)

        # Save UI
        st.markdown("### 💾 Save this scenario")
        st.text_input("Scenario name", key="scenario_name")

        if st.button("Save Scenario"):
            name = st.session_state.get("scenario_name", "").strip()

            if not name:
                st.warning("Please enter a name before saving.")
            elif name in st.session_state.scenarios:
                st.warning("Scenario name already exists. Please choose a unique name.")
            else:
                st.session_state.scenarios[name] = latest
                st.success(f"Scenario '{name}' saved.")
                st.write("📦 Scenarios stored:", list(st.session_state.scenarios.keys()))

        st.markdown("You can now compare this scenario with others in the **Scenario Comparison** tab.")
