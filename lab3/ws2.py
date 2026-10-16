import requests
from datetime import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json


# IDESCAT Excercise:
# Extract the following data from the onomástica table from the Idescat API:
# 1. Total number of females born in Catalonia in each of the last 5 years
# 2. Rank of the name María (id=40683) among newborn females in each of the last 5 years.
# 3. Absolute frecuency of the name María among newborns in each of the last 5 years.
# 4. Number of newborns per thousand named María in each of the last 5 years.
# 5. Number of newborns per thousand among females named María in each of the last 5 years.
#
# For each of these statistics, build a plot with the information.
# Obtain also the city in Catalonia where more Marías were born in each of the last 5 years.


# onomastica is the service we are instructed to used
# nadons is the subservice with newborn data
# dades is the operations which allows us to ask for statistics about a certain name or surname
# .json means we want our answers to be in json format

dades = "https://api.idescat.cat/onomastica/v1/nadons/dades.json" # URL of the service we are going to query

# Strategy: Statistics 2, 3, 4, 5 are about the name María. We will query the database using dades and get this data directly.
# Using statistics 3 and 5 we can obtain statistic 1 as: totalFemales = totalMarias / mariasPerThousandFemales * 1000
# The statistic about the city will be obtained by doing a different query, also to dades, using the class com. 

session = requests.Session()
r = session.get(dades, params={"id": 40683, "class": "t", "lang": "en"}) # We query dades and ask about the name María (id:40683). 
# Class t returns statistics filtered by year
# lang en means we want the data in english, not in cataln or spanish

r.raise_for_status() # If the query fails, this will raise a warning

data = r.json() # We store the output of the query as a json
years = data["onomastica_nadons"]["ff"]["f"] # The ff element contains one f row for each year there is data available. We store the data in an array.
last5 = years[-5:] # We select the relevant years from this vector, ie, the last five entries.



top_county = {}
for year in ["2021","2022","2023","2024","2025"]:
    county = {}
    r = session.get(dades, params={"id": 40683, "class": "com", "t": year, "lang": "en"}) # Query with the county (com) class to obtain by county data.
    # As we are not querying with the t class, we have to run the query several times, one per year.
    r.raise_for_status()
    data = r.json()["onomastica_nadons"]["ff"]["f"] # Store the data in an array. Each element corresponds to one county
    for c in data:
        if isinstance(c["c"], dict) and c["pos1"]["v"].isdigit(): # Check the county data is not empty (it can be empty for privacy reasons in small counties)
            name = c["c"]["content"]
            county[name] = int(c["pos1"]["v"]) # Store the number of Marias born
    top_county[year] = max(county, key=county.get)


# The relevant elements of each vector are the following
# c: year
# rank.sex: rank of the name among females
# pos1.v: absolute frequecy of the name
# pos1.w: relative frequecy (per thousand) of the name
# pos1.w.sex: relative frequency (per thousand) among females of the name

print("\nStatistics about the name María in Catalonia in the last 5 years (with available data)")

# We will now build a dataframe containing the relevant statistics for each year.
rows = []
for y in last5: # We build each row separately and then assemble the dataframe.
    v = float(y["pos1"]["v"]) # Absolute frequecy
    w = y["pos1"]["w"] # Relative frequency (per thousand)
    year = y["c"]
    rows.append({
        "Year": int(year),
        "Total female births": round(v / float(w["sex"]) * 1000),
        "Rank among females": int(y["rank"]["sex"]),
        "Frequency": v,
        "Newborns per thousand": float(w["total"]),
        "Newborns per thousand among females": float(w["sex"]),
        "County where the most Marias where born": top_county[year]
    })
df = pd.DataFrame(rows)

# We print the dataframe as a table. These options force python to print the whole dataframe and adjust it to the terminal window.
pd.set_option("display.max_columns", None)  
pd.set_option("display.width", None)        
print(df)

# Plotting the data from the data frame. One plot for each variable.
cols = [c for c in df.columns if c != "Year" and  c!= "County where the most Marias where born"]

for col in cols:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(df["Year"], df[col], color="#2a6fdb", linewidth=2, marker="o", markersize=7)
    ax.set_title(f"{col}")
    ax.set_xlabel("Year")
    ax.set_ylabel(col)
    ax.set_xticks(df["Year"])
    ax.grid(axis="y", color="#e5e5e5", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    if "Rank" in col:
        ax.invert_yaxis()  
    fig.tight_layout()

plt.show()

# Printing the county in which the most Marias were born each year.
for i in range(5):
    print(f"The county where the most Marias were born in the year {df['Year'][i]} was {df["County where the most Marias where born"][i]}.")