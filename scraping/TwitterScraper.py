import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://twitter.com/search?q='
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=options)

with open('books.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    book_id = []
    titles = []
    isbnList = []
    authorList = []
    comAuthorList = []
    comContentList = []
    count = 0
    for row in csv_reader:
        if count < 4000:
            count += 1
            continue
        title = str(row['title'])

        print('The title is: ' + title)

        url2 = url + title

        print url2

        driver.get(url2)

        print('debugging')
        time.sleep(1)
        page = driver.page_source

        soup = BeautifulSoup(page, 'html.parser')

        #print soup

        book_id.append(row['book_id'])
        isbnList.append(row['isbn'])
        titles.append(row['title'])
        authorList.append(row['authors'])



        review = soup.findAll('p', attrs={'class': 'TweetTextSize js-tweet-text tweet-text'})

        print('reviews')
        for i in review:
            print i.text.strip().encode("utf-8");
            print('______________________________________________________________')

        comContent = []
        for i in range (0,11):
            if(len(review) > i):
                comContent.append(review[i].text.strip().encode("utf-8"))

        for i in range (11,1):
            if(len(review) < i):
                comContent.append('none')

        comContentList.append(comContent)

        line_count += 1
        print(line_count)
        if line_count == 1000:
            driver.quit()
            break

    print(line_count)

'''
    j = 0
    for i in comContentList:
        while j < 10:
            print i[j]
            print('+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+')
            j += 1
'''

with open('twitterResult5.csv', mode= 'w') as testing_file:
    testing_writer = csv.writer(testing_file, delimiter = ',', quotechar= '"', quoting = csv.QUOTE_MINIMAL)
    testing_writer.writerow(['book_id', 'titles', 'isbn', 'author', 'review source', 'review content'])
    a = 0
    #j = 0
    while(a < line_count):
        for i in comContentList[a]:
            testing_writer.writerow([book_id[a], titles[a], isbnList[a], authorList[a], 'Twitter', i])
        a += 1
#
# print soup
# review1 = soup.findAll('div', attrs={'class': 'gig-comment-body'})
# for review in review1:
#     print(review.text)