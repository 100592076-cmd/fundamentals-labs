import requests
from datetime import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

URL='https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ei_bsco_m?format=JSON&unit=BAL&indic=BS-CSMCI&s_adj=SA&lang=EN'

# Now we obtain JSON data from API

response=requests.get(URL)
# We check if response_status is correct  
if response.status_code==200:
    data=response.json()
else:
    raise Exception (f"Wrong request or eurostat error. The response code was {response.status_code}")

# We extract dictionaries
geo_index=data["dimension"]["geo"]["category"]["index"] # Dictionary which assigns each country an index
time_index=data["dimension"]["time"]["category"]["index"]# Dictionary which assigns each date an index
values = data["value"] # Dictionary which assigns consumer confidence indicator values an index

dates = sorted(time_index.keys(), key=lambda k: time_index[k]) # We sort by index
n_dates = len (dates) # Total name of months available in the dataset

# Now we obtain DataFrame for european union, whose index is (EU27_2020)
# For obtaining the time series, we have to take into account that, for each value,
# its id is accesed doing
# id_val=(country_index · n_date) + date_index
pos_ue = geo_index["EU27_2020"]
ue_ts = []
for pos_f, f in enumerate(dates):
    id_val = str(pos_ue * n_dates + pos_f)
    ue_ts.append((f, values.get(id_val)))

# We transform the list of tuples (date, value) into a pandas dataframe
df_ue = pd.DataFrame(ue_ts, columns=["dates", "values"])

# We treat dates as time objects and values as numerical objects
df_ue["dates"] = pd.to_datetime(df_ue["dates"], format="%Y-%m")
df_ue["values"] = pd.to_numeric(df_ue["values"])

# Extra column in order to group by years later
df_ue["year"] = df_ue["dates"].dt.year

# We do the same process for Spain's data
pos_esp = geo_index["ES"]
esp_ts = []
for pos_f, f in enumerate(dates):
    id_val = str(pos_esp * n_dates + pos_f)
    esp_ts.append((f, values.get(id_val)))

df_esp = pd.DataFrame(esp_ts, columns=["dates", "values"])
df_esp["dates"] = pd.to_datetime(df_esp["dates"], format="%Y-%m")
df_esp["values"] = pd.to_numeric(df_esp["values"])
df_esp["year"] = df_esp["dates"].dt.year

# Last month we have is september 2026, so if we want 5 years we take 2022-2026

# 5. Calculate the required metrics
ue_5_years = df_ue[(df_ue["year"] >= 2022) & (df_ue["year"] <= 2026)].groupby("year", as_index=False)["values"].mean()

df_ue_2024 = df_ue[df_ue["year"] == 2024].copy()
df_ue_2024["month"] = df_ue_2024["dates"].dt.strftime("%Y-%m")
ue_monthly_2024 = df_ue_2024.groupby("month", as_index=False)["values"].mean()

df_esp_2024 = df_esp[df_esp["year"] == 2024].copy()
df_esp_2024["month"] = df_esp_2024["dates"].dt.strftime("%Y-%m")
esp_monthly_2024 = df_esp_2024.groupby("month", as_index=False)["values"].mean()

# 6Graphics
plt.figure(figsize=(7, 4))
bars1 = plt.bar(ue_5_years['year'].astype(str), ue_5_years['values'])
plt.title('EU Consumer Confidence – Last 5 Years (Yearly Mean)')
plt.xlabel('Year')
plt.ylabel('Index')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')

for bar in bars1:
    v = bar.get_height()
    va = 'bottom' if v >= 0 else 'top'
    plt.text(bar.get_x() + bar.get_width() / 2, v, f'{v:.1f}', ha='center', va=va, fontsize=9)

# Graphic 2: EU Monthly 2024
plt.figure(figsize=(8, 4))
bars2 = plt.bar(ue_monthly_2024['month'], ue_monthly_2024['values'])
plt.title('EU Consumer Confidence – 2024 Monthly Mean')
plt.xticks(rotation=45)
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')

for bar in bars2:
    v = bar.get_height()
    va = 'bottom' if v >= 0 else 'top'
    plt.text(bar.get_x() + bar.get_width() / 2, v, f'{v:.1f}', ha='center', va=va, fontsize=8)

# Gráfico 3: Spain Monthly 2024
plt.figure(figsize=(8, 4))
bars3 = plt.bar(esp_monthly_2024['month'], esp_monthly_2024['values'])
plt.title('Spain Consumer Confidence – 2024 Monthly Mean')
plt.xticks(rotation=45)
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')

for bar in bars3:
    v = bar.get_height()
    va = 'bottom' if v >= 0 else 'top'
    plt.text(bar.get_x() + bar.get_width() / 2, v, f'{v:.1f}', ha='center', va=va, fontsize=8)

plt.tight_layout()
plt.show()
