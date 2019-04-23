from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import requests
from xml.etree import ElementTree
import urllib

df = pd.read_csv("./bookdata.csv", header = 0 , index_col= 0)
url = "https://www.goodreads.com/book/title.xml?key=wHOxnq8b1uO8197pz7V7g&title="

isbn13s = []
booktitles = []

count=0

for index,row in df.iterrows():
    call = row['title'].split("(")[0]
    req  = urllib.quote_plus(call)
    response = requests.get(url+req)
    root = ElementTree.fromstring(response.content)
    try:
        isbn = root[1][3].text
        isbn13s.append(isbn)
        booktitles.append(row['title'])
    except:
        print(row['title']+"failed")
    print(count, isbn)
    count+=1

export = pd.DataFrame()
export['title'] = booktitles
export['isbn13'] = isbn13s

export.to_csv('./isbn13.csv', encoding='utf-8')
