from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome()

def sign_in(username, pas):
    driver.get("https://www.goodreads.com/user/sign_in")

    email = driver.find_element_by_xpath('//*[@id="user_email"]')
    password = driver.find_element_by_xpath('//*[@id="user_password"]')
    submit = driver.find_element_by_xpath('//*[@id="emailForm"]/form/fieldset/div[5]/input')

    email.send_keys(username)
    password.send_keys(pas)
    submit.click()

def clean(s):
    return s.encode("utf-8")

books = ["Pride And Prejudice",
    "To Kill A Mockingbird",
    "The Hobbit",
    "The Lord Of the Rings",
    "The Giver",
    "Lord Of The Flies",
    "The Princess Bride",
    "Slaughterhouse Five",
    "As I Lay Dying",
    "1984",
    "Frankenstein",
    "Great Expectations",
    "Heart of Darkness",
    "The Great Gatsby"]

sign_in('wesclock777@gmail.com', 'apples')

authors = []
ratings = []
descriptions = []
buy = []
covers = []
det = []

for book in books:
    driver.get('https://www.goodreads.com/')
    search = driver.find_element_by_xpath("/html/body/div[3]/div/header/div[1]/div/div[2]/form/input")
    search.click()
    search.send_keys(book)
    search.send_keys(Keys.RETURN)
    first_res = driver.find_element_by_xpath(   \
        "/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/table/tbody/tr[1]/td[2]/a/span")
    first_res.click()
    try:
        more = driver.find_element_by_xpath('//*[@id="description"]/a')
        more.click()
    except:
        pass

    try:
        more_details = driver.find_element_by_xpath('//*[@id="bookDataBoxShow"]')
        more_details.click()
    except:
        pass

    pic = driver.find_element_by_xpath('//*[@id="coverImage"]')
    covers.append(clean(pic.get_attribute("src")))

    des = driver.find_element_by_xpath('//*[@id="description"]')
    descriptions.append(clean(des.get_attribute("innerText")))

    auth = driver.find_element_by_xpath('//*[@id="bookAuthors"]/span[2]/div[1]/a/span')
    authors.append(clean(auth.get_attribute('innerHTML')))

    rating = driver.find_element_by_xpath('//*[@id="bookMeta"]/span[2]')
    ratings.append(clean(rating.get_attribute('innerHTML')))

    pgs = driver.find_element_by_xpath('//*[@id="details"]/div[1]')
    det.append(clean(pgs.get_attribute('innerText')))

    buybtn = driver.find_element_by_xpath('//*[@id="buyButton"]')
    buy.append(clean(buybtn.get_attribute('href')))
driver.quit()

df = pd.DataFrame()

df['title'] = books
df['author'] = authors
df['rating'] = ratings
df['cover'] = covers
df['details'] = det
df['description'] = descriptions
df['purchase'] = buy

df.to_csv('bookdata.csv')

print df.head(14)
