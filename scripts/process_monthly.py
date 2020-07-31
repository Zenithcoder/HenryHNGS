from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pandas import DataFrame
import csv
import pandas as pd
from urllib.request import urlopen
import datetime

try:
    html = urlopen("https://www.eia.gov/dnav/ng/hist/rngwhhdM.htm")
except HTTPError as e:
    print(e)
except URLError:
    print("Server down")
else:
    res = BeautifulSoup(html.read(), "html5lib")

table = None
table = res.findAll("table")[5]

monthly_price_list = []
date_list = []

#first_rows = table.findAll("tr")[0]
first_rows = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
    'Nov', 'Dec'
]
rows = table.findAll("tr")[1:]
print(first_rows)
for row in rows:
    date = None
    cells = row.findAll("td")
    if cells[0].get("class") == None: continue
    if "B4" in cells[0].get("class"):
        d = cells[0].getText().strip()
        for i, cell in enumerate(cells):
            if "B3" in cell.get("class"):
                price = cell.getText().strip()
                if price == "" or price == "NA": price = ""
                else: price = float(price)
                monthly_price_list.append(price)
                date_list.append(first_rows[i - 1] + "-" + d)

d1 = pd.DataFrame({'Date': date_list})
d2 = pd.DataFrame({'Price': monthly_price_list})
df = pd.concat([d1, d2], axis=1)
print(df)
df.to_csv(r"data/monthly.csv", index=False, header=True)
