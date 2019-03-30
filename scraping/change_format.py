import pandas as pd

df = pd.read_csv("./newbookdata.csv", header = 0, index_col = 0)
df.to_csv('./newbookdata_formatted.csv', encoding='ascii', mode='a', header=False)
