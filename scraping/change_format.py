import pandas as pd

df = pd.read_csv("./newbookdata.csv", header = 0, index_col = 0)
print(df.dtypes)
df['description'] = df.description.str.decode('utf-8')
df['details'] = df.details.str.decode('utf-8')
df['title'] = df.title.str.decode('utf-8')
df['author'] = df.author.str.decode('utf-8')

df['description'] = df.description.str.encode("ascii","ignore")

df['details'] = df.details.str.encode("ascii","ignore")

df['title'] = df.title.str.encode("ascii","ignore")

df['author'] = df.author.str.encode("ascii","ignore")

# isbn                          object
# isbn13                         int64
# original_publication_year      int64
# title                         object
# average_rating               float64
# ratings_count                  int64
# work_ratings_count             int64
# work_text_reviews_count        int64
# ratings_1                      int64
# ratings_2                      int64
# ratings_3                      int64
# ratings_4                      int64
# ratings_5                      int64
# image_url                     object
# author                        object
# details                       object
# description                   object
# purchase                      object



df.to_csv('../newbookdata_formatted.csv', encoding='ascii', header=True)
