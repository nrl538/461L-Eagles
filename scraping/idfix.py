import pandas as pd
import sys

reload(sys)
sys.setdefaultencoding('utf8')

books = pd.read_csv("./books.csv", header = 0)

bookdata = pd.read_csv("./bookdata.csv", header = 0)

book_ids = []

for index, row in bookdata.iterrows():
    temp = row['title'].strip()
    df = books[books['title'].str.strip()==temp]
    try:
        book_ids.append(df.index[0]+1)
    except:
        print(row['title'], index)
        break


bookdata['book_id'] = book_ids
bookdata.drop_duplicates(subset=['title'])
bookdata.to_csv('./bookdata_fixed.csv', encoding='utf-8', header=True, index=False)
