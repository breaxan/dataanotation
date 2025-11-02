import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://docs.google.com/document/d/e/2PACX-1vSZ9d7OCd4QMsjJi2VFQmPYLebG2sGqI879_bSPugwOo_fgRcZLAFyfajPWU91UDiLg-RxRD41lVYRA/pub"

driver = webdriver.Firefox()
driver.get(url)

rows = driver.find_elements(By.CSS_SELECTOR, "tr")[1:]
table = []
for i, row in enumerate(rows):
    cols = row.find_elements(By.CSS_SELECTOR, "td")
    table_row = []
    for j, col in enumerate(cols):
        val = col.text
        if j == 1:
            table_row.append(val)
        else:
            table_row.append(int(val))
    table.append(table_row)

driver.close()

df = pd.DataFrame(table, columns=["x-coordinate", "character", "y-coordinate"])
df.sort_values(["y-coordinate", "x-coordinate"], ascending=[False, True], inplace=True, ignore_index=True)

x_lim = df["x-coordinate"].max()
y_lim = df["y-coordinate"].max()
for i in range(y_lim + 1):
    for j in range(x_lim + 1):
        x = j
        y = y_lim - i
        sub_df = df[(df["x-coordinate"] == x) & (df["y-coordinate"] == y)].reset_index()
        if not sub_df.empty:
            print(sub_df.at[0, "character"], end="")
        else:
            print(" ", end="")
    print("")