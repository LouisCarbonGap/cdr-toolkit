import pandas as pd

method_groups = {
    "Forestry": [
        "Forestry", "Forest management", "Agroforestry"],
    "Soil carbon sequestration (crop, grasslands)": [
        "Cropland management", "Pasture management"],
    "Blue carbon": [
        "Coastal revegetation (mangrove, seaweeds…)"],
    "Durable biobased products": [
        "Durable biobased products"],
    "Bio-char": [
        "Bio-char - Forest biomass", "Bio-char - Non-forest biomass", "Bio-char - Unspecified biomass"
    ],
    "Bio-CCS": [
        "BioCCS with combustion", "BioCCS with combustion & growing biomass", "BioCCS with anaerobic digestion/fermentation", "BioCCS with anaerobic digestion/fermentation & growing biomass"
    ],
    "Enhanced weathering": [
        "Enhanced weathering - Basalt mineral", "Enhanced weathering - Olivine mineral", "Enhanced weathering - Wollastonite mineral", "Enhanced weathering - Unspecified mineral"
    ],
    "Ocean alkalinity enhancement": [
        "Mineral OAE / Ocean liming", "Electrochemical OAE"
    ],
    "Direct air carbon capture and storage (DACCS)": [
        "Electrochemical DACCS", "Low-temp DACCS (solid-sorbent/liquid-solvent)",
        "High-temp DACCS (solid-sorbent/liquid-solvent)", "Mineral looping DACCS",
        "Moisture swing DACCS"
    ],
    "Direct ocean carbon captureand storage (DOCCS)": ["pH swing"],
    "Mineralization": ["Mineralization ex-situ"]
}

resource_groups = {
    "Minerals": ["Basalt mineral (t/tCO2)", "Olivine mineral (t/tCO2)", "Wollastonite mineral (t/tCO2)", "Unspecified mineral (t/tCO2)"],
    "Biomass": ["Forest biomass (t/tCO2)", "Non-forest biomass (t/tCO2)", "Unspecified biomass (t/tCO2)"],
    "Land": ["Arable land (ha/tCO2)", "Non-arable land (ha/tCO2)", "Unspecified land (ha/tCO2)"],
    "Chemicals": ["Unspecified chemical (t/tCO2)"],
    "Energy": ["Electrical energy (MWh/tCO2)", "Thermal energy (MWh/tCO2)"],
    "Water": ["Salt water (Liters/tCO2)", "Unspecified water (Liters/tCO2)"],
    "Shoreline": ["Shoreline (km/tCO2)"],
}

method_order = sum(method_groups.values(), [])

resource_order = sum(resource_groups.values(), [])

# names used for display
resource_unit_map = {
    "Land": "ha",
    "Energy": "MWh",
    "Biomass": "t",
    "Minerals": "t",
    "Chemicals": "t",
    "Shoreline": "km",
    "Water": "L"
}

resource_grouped = {
    "Land": ["Arable land (ha/tCO2)", "Non-arable land (ha/tCO2)", "Unspecified land (ha/tCO2)"],
    "Energy": ["Electrical energy (MWh/tCO2)", "Thermal energy (MWh/tCO2)"],
    "Biomass": ["Forest biomass (t/tCO2)", "Non-forest biomass (t/tCO2)", "Unspecified biomass (t/tCO2)"],
    "Minerals": ["Basalt mineral (t/tCO2)", "Olivine mineral (t/tCO2)", "Wollastonite mineral (t/tCO2)", "Unspecified mineral (t/tCO2)"],
    "Chemicals": ["Unspecified chemical (t/tCO2)"],
    "Shoreline": ["Shoreline (km/tCO2)"],
    "Water": ["Salt water (Liters/tCO2)", "Unspecified water (Liters/tCO2)"]
}

# secondary resources
secondary_df = pd.read_csv("data/secondary_resources.csv")
secondary_resources = set(zip(secondary_df["method"], secondary_df["resource"]))