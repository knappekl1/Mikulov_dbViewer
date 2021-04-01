import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

#get db from HEROKU into DataFrame
#load config
configPath = "config.json"

#print(os.path.abspath(configPath))

with open (configPath,"r") as file:
    configObj = json.load(file)

engineString = f'postgresql+psycopg2://{configObj["userName"]}:{configObj["password"]}@{configObj["hostName"]}/{configObj["databaseName"]}'
engine = create_engine(engineString)

#fetch data from DB
with engine.connect() as conn:
    query = "REFRESH MATERIALIZED VIEW day_ma7;"
    conn.execute(query)
    selectQuery = "SELECT * FROM day_ma7"
    result = conn.execute(selectQuery).fetchall()

#Create DataFrame from DB Data (cannot use pd.read_sql directly as it does not support reading from View)
df = pd.DataFrame(data = result, columns = ["item_date", "consumption","ma7"])
df["item_date"] = pd.to_datetime(df["item_date"])
df = df.sort_values("item_date")
dfMax = df.sort_values("consumption", ascending=False)[:5]
print(dfMax)

fig = plt.figure(figsize=(18,8))
gs = fig.add_gridspec(2,2)
ax1 = fig.add_subplot(gs[0,:])
ax1.plot(df["item_date"], df["consumption"])
ax1.plot(df["item_date"], df["ma7"])
ax1.grid(axis="y", lw=0.5)
ax1.set_title("Denní Spotřeba (kWh")
ax2 = fig.add_subplot(gs[1,0])
ax2.bar(range(0, len(dfMax.index)),height=dfMax["consumption"])
ax2.set_xticklabels(dfMax["item_date"])
ax2.set_title("TOP 5 Spotřeba")
plt.tight_layout()
plt.show()

# fig, ax = plt.subplots(figsize=(24,8)) # simplest way to create fig obj and axes
# ax.plot(df["item_date"], df["consumption"])
# ax.plot(df["item_date"], df["ma7"])
# ax.set_xlabel("Date")
# plt.title("Denní spotřeba (kWh)")
# plt.grid(axis="y", lw=0.5)
# plt.tight_layout()
# plt.show()