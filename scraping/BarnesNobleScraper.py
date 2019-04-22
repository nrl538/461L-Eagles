import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

'''
#!/usr/bin/env python
print('If you get error "ImportError: No module named \'six\'"'+\
    'install six:\n$ sudo pip install six');
import sys
if sys.version_info[0]==2:
    import six
    from six.moves.urllib import request
    opener = request.build_opener(
        request.ProxyHandler(
            {'http': 'http://127.0.0.1:24000'}))
    print(opener.open('http://lumtest.com/myip.json').read())
if sys.version_info[0]==3:
    import urllib.request
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler(
            {'http': 'http://127.0.0.1:24000'}))
    print(opener.open('http://lumtest.com/myip.json').read())
'''



with open('books.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    count = 0
    tracking = 2050
    tracking2 = 21
    repeat = 0
    while repeat < 70:
        book_id = []
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

        url = 'https://www.barnesandnoble.com/s/'
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=options)


        line_count = 0
        tracking += 100
        tracking2 += 1
        repeat += 1
        count = 0

        for row in csv_reader:
            if count < tracking:
                count += 1
                continue
            #isbn = '0385534639'
            isbn = str(row['isbn'])
            while(len(isbn) < 10):
                isbn = '0' + isbn
            print('The isbn is: ' + isbn)

            url2 = url + isbn
            #url2 = 'https://www.barnesandnoble.com/w/1984-george-orwell/1100009100?ean=9780451524935'
            driver.get(url2)
            time.sleep(2)
            page = driver.page_source

            soup = BeautifulSoup(page, 'html.parser')

            #print soup

            avgRating = soup.find('span', attrs={'class': 'average'})

            if avgRating is None:
                avgRating = soup.find('span', attrs={'class': 'gig-average-review'})
                if avgRating is None:
                    print('___________ isbn invalid, searching by titles... ________________')
                    url3 = url + row['title']
                    print(url3)
                    driver.get(url3)
                    time.sleep(1)
                    page = driver.page_source
                    soup = BeautifulSoup(page, 'html.parser')

                    avgRating = soup.find('span', attrs={'class': 'average'})
                    if avgRating is None:
                        avgRating = soup.find('span', attrs={'class': 'gig-average-review'})
                    if avgRating is None:
                        #print soup
                        print ('__________________ link found by title search ___________________')
                        links = soup.find('a', attrs={'class': 'pImageLink'})
                        if links is None:
                            print ('____________ Try Again ____________')
                            time.sleep(30)
                            driver.get(url3)
                            page = driver.page_source
                            soup = BeautifulSoup(page, 'html.parser')
                            links = soup.find('a', attrs={'class': 'pImageLink'})
                            if links is None:
                                print ("no link")
                                tracking += 1
                                print soup
                                continue

                        a = str(links.get('href'))
                        url4 = 'https://www.barnesandnoble.com' + a
                        print url4
                        driver.get(url4)
                        time.sleep(1)
                        page = driver.page_source
                        soup = BeautifulSoup(page, 'html.parser')

            #print soup

            book_id.append(row['book_id'])
            isbnList.append(isbn)
            titles.append(row['title'])
            authorList.append(row['authors'])
            avgRating = soup.find('span', attrs={'class': 'average'})
            if avgRating is None:
                avgRating = soup.find('span', attrs={'class': 'gig-average-review'})
                if avgRating is None:
                    print soup
                    continue
            print(avgRating.text.encode("utf-8"))
            avgRatingList.append(avgRating.text.encode("utf-8"))
            reviewAuthor = soup.findAll('td', attrs={'class': 'gig-comment-username'})
            if len(reviewAuthor) == 0:
                reviewAuthor = soup.findAll('span', attrs={'class': 'gig-comment-username'})
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
            print(line_count)
            if line_count >= 100:
                driver.quit()
                break

        print(line_count)


        with open("B&Nresult" + str(tracking2) + ".csv", mode= 'w') as testing_file:
            testing_writer = csv.writer(testing_file, delimiter = ',', quotechar= '"', quoting = csv.QUOTE_MINIMAL)
            testing_writer.writerow(['book_id', 'titles', 'isbn', 'author', 'review source', 'average rating', 'review author', 'review content'])
            a = 0
            while(a < line_count):
                testing_writer.writerow([book_id[a], titles[a], isbnList[a], authorList[a], 'Barnes and Noble', avgRatingList[a], comAuthor1[a], comContent1[a]])
                testing_writer.writerow([book_id[a], titles[a], isbnList[a], authorList[a], 'Barnes and Noble', avgRatingList[a], comAuthor2[a], comContent2[a]])
                testing_writer.writerow([book_id[a], titles[a], isbnList[a], authorList[a], 'Barnes and Noble', avgRatingList[a], comAuthor3[a], comContent3[a]])
                a += 1
        time.sleep(150)


'''
    print(titles[0])
    print(isbnList[0])
    print(authorList[0])
    print(comAuthor1[0])
    print(comContent1[0])
    print(comAuthor2)
    print(comContent2)
    print(comAuthor3)
    print(comContent3)
    print(avgRatingList)
'''

#
# print soup
# review1 = soup.findAll('div', attrs={'class': 'gig-comment-body'})
# for review in review1:
#     print(review.text)


