import pandas as pd

# params
background_color = "#185d0a"

def styled_table(df):
    return (
        df.style
        .set_table_styles([{"selector": "th", "props": [("background-color", background_color), ("font-weight", "bold")]}])
    )

def highlight_differences(data, df_default):
    styled = pd.DataFrame('', index=data.index, columns=data.columns)
    for m in data.index:
        for r in data.columns:
            if m in df_default.index and r in df_default.columns:
                current = data.at[m, r]
                default = df_default.at[m, r]
                if abs(current - default) > 1e-6:
                    styled.at[m, r] = 'background-color: #cce5ff'
    return styled

def smart_format(val):
    return f"{val:.2e}" if abs(val) < 0.01 else f"{val:.2f}"

def inputs_table_style(df):
    return(
        df.style
        .set_properties(**{'text-align': 'right'})
        .format(smart_format)
        .set_table_styles([{"selector": "th", "props": [("background-color", background_color), ("font-weight", "bold")]}])
    )
    
def format_resource_summary(df: pd.DataFrame):
    """
    Format a resource availability summary table with styling and column width control.
    """
    df = df.copy()
    df["Available Amount"] = df["Available Amount"].map(lambda x: f"{x:.2f}")
    df.index.name = "Resource"  # label the index for clarity

    return (
        df.style
            .set_table_styles([
                {
                    "selector": "thead th:nth-child(1)",  # First column header (after index)
                    "props": [
                        ("background-color", "#185d0a"),
                        ("color", "white"),
                        ("font-weight", "bold")
                    ]
                },
                {
                    "selector": "thead th:nth-child(2)",  # Second column header
                    "props": [
                        ("background-color", "#185d0a"),
                        ("color", "white"),
                        ("font-weight", "bold")
                    ]
                }
            ])
        )
    
def format_method_summary(df: pd.DataFrame):
    df = df.copy()
    df.index.name = "CDR Method"
    df.reset_index(inplace=True)

    return (
        df.style
        .set_table_styles([
            {"selector": "thead th", "props": [("background-color", background_color), ("color", "white"), ("font-weight", "bold")]},
            {"selector": "td.col0", "props": [("text-align", "left"), ("font-weight", "bold")]},
            {"selector": "td.col1", "props": [("text-align", "center")]}
        ])
    )
    
def format_results_summary(df: pd.DataFrame):
    df = df.copy()
    df.index.name = "CDR Method"
    df.reset_index(inplace=True)

    return (
        df.style
        .format({
            "tCO₂ removed": "{:,.0f}",
            "Share (%)": "{:.2f}"
        })
        .set_table_styles([
            {"selector": "thead th", "props": [("background-color", background_color), ("color", "white"), ("font-weight", "bold")]},
            {"selector": "td.col0", "props": [("text-align", "left"), ("font-weight", "bold")]},
            {"selector": "td.col1", "props": [("text-align", "center")]}
        ])
    )
    
    
def format_efficiency_summary(df: pd.DataFrame, df_default: pd.DataFrame):
    df = df.copy()
    df.index.name = "Method"

    # Highlight changes first
    styled = df.style.apply(lambda d: highlight_differences(d, df_default), axis=None)

    # Apply table styles
    num_columns = df.shape[1]
    styles = [
        {
            "selector": "thead th",
            "props": [
                ("background-color", background_color),
                ("color", "white"),
                ("font-weight", "bold")
            ]
        },
        {
            "selector": "th.row_heading",
            "props": [
                ("text-align", "left"),
                ("font-weight", "bold"),
                ("width", "240px")
            ]
        }
    ]

    for i in range(num_columns):
        styles.append({
            "selector": f"td.col{i}",
            "props": [
                ("text-align", "center"),
                ("width", "160px")
            ]
        })

    # Add 2-decimal formatting
    return styled.set_table_styles(styles).format("{:.2f}")


def format_results_table(df: pd.DataFrame):
    """
    Style the results table (e.g., optimization output) with formatting consistent with other tables.
    """
    df = df.copy()
    df.index.name = "Method"

    styles = [
        {
            "selector": "thead th",
            "props": [
                ("background-color", background_color),
                ("color", "white"),
                ("font-weight", "bold")
            ]
        },
        {
            "selector": "th.row_heading",
            "props": [
                ("text-align", "left"),
                ("font-weight", "bold"),
                ("width", "240px")
            ]
        },
        {
            "selector": "td",
            "props": [
                ("text-align", "center"),
                ("font-size", "14px")
            ]
        }
    ]

    return (
        df.style
        .set_table_styles(styles)
        .format("{:.2f}")
    )

