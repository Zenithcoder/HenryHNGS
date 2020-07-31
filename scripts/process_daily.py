from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pandas import DataFrame
import csv
import pandas as pd
from urllib.request import urlopen
import datetime

try:
    html = urlopen("https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm")
except HTTPError as e:
    print(e)
except URLError:
    print("Server down")
else:
    res = BeautifulSoup(html.read(), "html5lib")

table = None
for t in res.findAll("table"):
    table = t if "summary" in t.attrs else table
if table == None: exit()

daily_price_list = []
date_list = []

rows = table.findAll("tr")[1:]
for row in rows:
    date = None
    cells = row.findAll("td")
    if cells[0].get("class") == None: continue
    if "B6" in cells[0].get("class"):
        d = cells[0].getText().split(" to ")[0].strip().replace(" ", "")
        date = datetime.datetime.strptime(d, "%Y%b-%d")
        for cell in cells:
            if "B3" in cell.get("class"):
                price = cell.getText().strip()
                if price == "" or price == "NA": price = ""
                else: price = float(price)
                daily_price_list.append(price)
                date_list.append(date)
                date = date + datetime.timedelta(days=1)

d1 = pd.DataFrame({'Date': date_list})
d2 = pd.DataFrame({'Price': daily_price_list})
df = pd.concat([d1, d2], axis=1)
print(df)
df.to_csv(r"data/daily.csv", index=False, header=True)
