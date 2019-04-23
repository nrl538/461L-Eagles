import pandas as pd
import sys

reload(sys)
sys.setdefaultencoding('utf8')

bookdata = pd.read_csv("./bookdata_fixed.csv", header = 0)
isbn = pd.read_csv("./isbn13.csv", dtype={0:'int8',1:'object',2:'object'},header = 0, index_col=0)
isbn = isbn.dropna(axis=0)

book_ids = []

print(isbn.head())

for index, row in bookdata.iterrows():
    temp = row['title'].strip()
    df = isbn[isbn['title'].str.strip()==temp]
    try:
        isbn13 = df.isbn13.tolist()[0]
    except:
        continue
    if isbn13 != 'nan' and isbn13 != "" and isbn13 !=None:
        bookdata.at[index,'isbn13'] = str(isbn13)
    else: continue

bookdata = bookdata.drop_duplicates(subset=['title'])
bookdata.to_csv('./bookdata_fixed2.csv', encoding='utf-8', header=True, index=False)
