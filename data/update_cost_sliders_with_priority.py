import json

import pandas as pd

# === Load JSON data ===
with open("cost_sliders.json", "r") as f:
    cost_sliders = json.load(f)

# === Load resource priority CSV ===
df_priority = pd.read_csv("resource_priority.csv")

# === Validate columns ===
required_cols = {"method", "resource", "priority"}
if not required_cols.issubset(df_priority.columns):
    raise ValueError(f"CSV must contain the columns: {required_cols}")

# === Update the JSON structure ===
for _, row in df_priority.iterrows():
    method = row["method"]
    resource = row["resource"]
    priority = row["priority"]

    if method in cost_sliders and resource in cost_sliders[method]:
        cost_sliders[method][resource]["priority"] = priority
    else:
        print(f"⚠️ Warning: ({method} / {resource}) not found in JSON.")

# === Save the updated JSON ===
with open("cost_sliders_with_priority.json", "w") as f:
    json.dump(cost_sliders, f, indent=2)

print("✅ Updated JSON saved to cost_sliders_with_priority.json")
