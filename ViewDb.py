import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from datetime import datetime

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
#Create DF with top 5 values
dfMax = df.sort_values("consumption", ascending=False)[:5]
#Create DF with last 30 values, ascending
df30 = df[-30:]


myData = []
for val in dfMax[["item_date","consumption"]].itertuples():
    myData.append([val[1].strftime('%d.%m.%Y'),val[2]])



fig = plt.figure(figsize=(18,8))
gs = fig.add_gridspec(2,2)
ax1 = fig.add_subplot(gs[0,:])
ax1.plot(df["item_date"], df["consumption"], label="Spotřeba")
ax1.plot(df["item_date"], df["ma7"], label="7denní průměr")
ax1.grid(axis="y", lw=0.5)
ax1.set_xlabel("Datum")
ax1.set_ylabel("kWh/den")
ax1.set_title("Denní Spotřeba (kWh)")
ax1.legend(loc=(0.01,0.78))
ax2 = fig.add_subplot(gs[1,0])
ax2.plot(df30["item_date"], df30["consumption"],color="green", label="Spotřeba")
ax2.plot(df30["item_date"], df30["ma7"], color="red", label="7denní průměr")
ax2.grid(axis="y", lw=0.5)
ax2.set_title("Spotřeba posledních 30 dní")
ax2.legend(loc=(0.8,0.8))
ax3 = fig.add_subplot(gs[1,1])
ax3.axis("tight")
ax3.axis("off")
ax3.table(cellText=myData, colLabels=["Date","Spotřeba (kWh)"], colLoc="right", colColours=["#3399FF","#3399FF"], loc='center')
ax3.set_title("TOP 5 Spotřeba")
plt.tight_layout()
plt.show()
