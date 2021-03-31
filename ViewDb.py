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

with engine.connect() as conn:
    query = "REFRESH MATERIALIZED VIEW day_ma7;"
    conn.execute(query)
    selectQuery = "SELECT * FROM day_ma7 LIMIT 10"
    result = conn.execute(selectQuery).fetchall()


df = pd.DataFrame(data = result, columns = ["item_date", "consumption","ma7"])
df["item_date"] = pd.to_datetime(df["item_date"])
dfMax = df.sort_values("consumption", ascending=False)[:5]
print(dfMax)

