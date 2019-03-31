import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://www.barnesandnoble.com/s/'
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=options)

with open('selectedbooks.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    titles = []
    isbnList = []
    authorList = []
    avgRatingList = []
    comAuthor1 = []
    comContent1 = []
    comAuthor2 = []
    comContent2 = []
    comAuthor3 = []
    comContent3 = []

    for row in csv_reader:
        isbn = str(row['isbn'])
        while(len(isbn) < 10):
            isbn = '0' + isbn
        print('The isbn is: ' + isbn)

        url2 = url + isbn
        driver.get(url2)
        time.sleep(1)
        page = driver.page_source

        soup = BeautifulSoup(page, 'html.parser')
        avgRating = soup.find('span', attrs={'class': 'average'})
        if(avgRating is None):
            print ('No result')
            continue
        isbnList.append(isbn)
        titles.append(row['title'])
        authorList.append(row['authors'])
        #avgRating = soup.find('span', attrs={'class': 'gig-average-review'})
        print(avgRating.text.encode("utf-8"))
        avgRatingList.append(avgRating.text.encode("utf-8"))

        reviewAuthor = soup.findAll('td', attrs={'class': 'gig-comment-username'})
        review = soup.findAll('div', attrs={'class': 'gig-comment-body'})

        if(len(reviewAuthor) > 0):
            comAuthor1.append(reviewAuthor[0].text.encode("utf-8"))
            comContent1.append(review[0].text.strip().encode("utf-8"))

            if (len(reviewAuthor) > 1):
                comAuthor2.append(reviewAuthor[1].text.encode("utf-8"))
                comContent2.append(review[1].text.strip().encode("utf-8"))
                if (len(reviewAuthor) > 2):
                    comAuthor3.append(reviewAuthor[2].text.encode("utf-8"))
                    comContent3.append(review[2].text.strip().encode("utf-8"))
        if(len(reviewAuthor) < 3):
            comAuthor3.append('none')
            comContent3.append('none')
            if (len(reviewAuthor) < 2):
                comAuthor2.append('none')
                comContent2.append('none')
                if (len(reviewAuthor) < 1):
                    comAuthor1.append('none')
                    comContent1.append('none')
        line_count += 1

        if line_count == 1000:
            driver.quit()
            break

    print(line_count)

    print(titles)
    print(isbnList)
    print(authorList)
    print(comAuthor1)
    print(comContent1)
    print(comAuthor2)
    print(comContent2)
    print(comAuthor3)
    print(comContent3)
    print(avgRatingList)


with open('result.csv', mode= 'w') as testing_file:
    testing_writer = csv.writer(testing_file, delimiter = ',', quotechar= '"', quoting = csv.QUOTE_MINIMAL)
    testing_writer.writerow(['titles', 'isbn', 'author', 'review source', 'average rating', 'review author', 'review content'])
    a = 0
    while(a < line_count):
        testing_writer.writerow([titles[a], isbnList[a], authorList[a], 'Barnes and Noble', avgRatingList[a], comAuthor1[a], comContent1[a]])
        testing_writer.writerow([titles[a], isbnList[a], authorList[a], 'Barnes and Noble', avgRatingList[a], comAuthor2[a], comContent2[a]])
        testing_writer.writerow([titles[a], isbnList[a], authorList[a], 'Barnes and Noble', avgRatingList[a], comAuthor3[a], comContent3[a]])
        a += 1

#
# print soup
# review1 = soup.findAll('div', attrs={'class': 'gig-comment-body'})
# for review in review1:
#     print(review.text)