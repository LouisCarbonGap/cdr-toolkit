#%% uses the latest version of aggregated inputs to create the dictionary of costs
import json
from os import name

import pandas as pd
from matplotlib import units
from numpy import append


def create_sliders_inputs():
    df = pd.read_csv("inputs_aggregated.csv")

    cost_sliders = {}

    # extract data from inputs and create final dictionary for sliders
    for _, row in df.iterrows():
        method = row["Implementation"]
        # break bio-char into 3 different cases, based on which biomass is used
        """
        For the Implementation "Biochar", we must create three different cases:
        1. Bio-char - Forest biomass
        2. Bio-char - Non-forest biomass
        3. Bio-char - Unspecified biomass
        Where we have to keep the value for the corresponding resource in:
            [Forest biomass OR Non-forest biomass OR Unspecified biomass]
        But set the other two to zero, and keep the values in the other resources intact
        """
        resource = row["Resource"] + " (" + row["Unit"] + ")"
        if row["min"] == row["max"]:
            row["min"] = row["min"] * .5
        entry = {
            "min": float(row["min"]),
            "median": float(row["median"]),
            "max": float(row["max"])
        }
        cost_sliders.setdefault(method, {})[resource] = entry
        
    print(cost_sliders)
    
    # create the three cases for bio-char
    cost_sliders["Bio-char - Forest biomass"] = cost_sliders["Bio-char"].copy()
    cost_sliders["Bio-char - Forest biomass"].pop("Non-forest biomass (t/tCO2)")
    cost_sliders["Bio-char - Forest biomass"].pop("Unspecified biomass (t/tCO2)")
    cost_sliders["Bio-char - Non-forest biomass"] = cost_sliders["Bio-char"].copy()
    cost_sliders["Bio-char - Non-forest biomass"].pop("Forest biomass (t/tCO2)")
    cost_sliders["Bio-char - Non-forest biomass"].pop("Unspecified biomass (t/tCO2)")
    cost_sliders["Bio-char - Unspecified biomass"] = cost_sliders["Bio-char"].copy()
    cost_sliders["Bio-char - Unspecified biomass"].pop("Forest biomass (t/tCO2)")
    cost_sliders["Bio-char - Unspecified biomass"].pop("Non-forest biomass (t/tCO2)")
    # remove "Bio-char" from the dictionary
    if "Bio-char" in cost_sliders:
        del cost_sliders["Bio-char"]
        
    # create all cases for enhanced weathering
    cost_sliders["Enhanced weathering - Basalt mineral"] = cost_sliders["Enhanced weathering"].copy()
    cost_sliders["Enhanced weathering - Basalt mineral"].pop("Olivine mineral (t/tCO2)")
    cost_sliders["Enhanced weathering - Basalt mineral"].pop("Wollastonite mineral (t/tCO2)")
    cost_sliders["Enhanced weathering - Basalt mineral"].pop("Unspecified mineral (t/tCO2)")
    cost_sliders["Enhanced weathering - Olivine mineral"] = cost_sliders["Enhanced weathering"].copy()
    cost_sliders["Enhanced weathering - Olivine mineral"].pop("Basalt mineral (t/tCO2)")
    cost_sliders["Enhanced weathering - Olivine mineral"].pop("Wollastonite mineral (t/tCO2)")
    cost_sliders["Enhanced weathering - Olivine mineral"].pop("Unspecified mineral (t/tCO2)")
    cost_sliders["Enhanced weathering - Wollastonite mineral"] = cost_sliders["Enhanced weathering"].copy()
    cost_sliders["Enhanced weathering - Wollastonite mineral"].pop("Basalt mineral (t/tCO2)")
    cost_sliders["Enhanced weathering - Wollastonite mineral"].pop("Olivine mineral (t/tCO2)")
    cost_sliders["Enhanced weathering - Wollastonite mineral"].pop("Unspecified mineral (t/tCO2)")
    cost_sliders["Enhanced weathering - Unspecified mineral"] = cost_sliders["Enhanced weathering"].copy()
    cost_sliders["Enhanced weathering - Unspecified mineral"].pop("Basalt mineral (t/tCO2)")
    cost_sliders["Enhanced weathering - Unspecified mineral"].pop("Olivine mineral (t/tCO2)")
    cost_sliders["Enhanced weathering - Unspecified mineral"].pop("Wollastonite mineral (t/tCO2)")
    # remove "Enhanced weathering" from the dictionary
    if "Enhanced weathering" in cost_sliders:
        del cost_sliders["Enhanced weathering"]    
    # create case for growing biomass in bioccs
    cost_sliders["BioCCS with combustion & growing biomass"] = cost_sliders["BioCCS with combustion"].copy()
    cost_sliders["BioCCS with combustion"].pop("Arable land (ha/tCO2)")
    cost_sliders["BioCCS with combustion & growing biomass"].pop("Forest biomass (t/tCO2)")
    cost_sliders["BioCCS with combustion & growing biomass"].pop("Unspecified biomass (t/tCO2)")
    
    cost_sliders["BioCCS with anaerobic digestion/fermentation & growing biomass"] = cost_sliders["BioCCS with anaerobic digestion/fermentation"].copy()
    cost_sliders["BioCCS with anaerobic digestion/fermentation"].pop("Arable land (ha/tCO2)")
    cost_sliders["BioCCS with anaerobic digestion/fermentation & growing biomass"].pop("Non-forest biomass (t/tCO2)")
    cost_sliders["BioCCS with anaerobic digestion/fermentation & growing biomass"].pop("Unspecified biomass (t/tCO2)")
    
    

    with open("cost_sliders.json", "w") as f:
        json.dump(cost_sliders, f, indent=2)

    print("Saved slider configuration to cost_sliders.json")

if __name__ == "__main__":
    create_sliders_inputs()
    print("Script executed successfully.")
# %%
