import urllib, json, time, csv

urlStart = "https://www.reddit.com/r/books/search.json?q="
urlEnd = "&sort=relevance&restrict_sr=on"

with open('books.csv', mode='r') as csv_file, open('RedditResults.csv', mode='w') as csv_in:
    csv_reader = csv.DictReader(csv_file)
    csv_writer = csv.writer(csv_in, delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['book_id', 'titles', 'isbn', 'author', 'review source', 'review author', 'review content'])
    """
    book_ids = []
    titles = []
    isbns = []
    authors = []
    postAuthors = []
    contents = []"""
    # test = 5
    for row in csv_reader:
        """
        book_ids.append(row['\xef\xbb\xbfbook_id'])
        titles.append(row['title'])
        isbns.append(row['isbn'])
        authors.append(row['authors'])"""

        print row['\xef\xbb\xbfbook_id']
        bookTitle = str(row['original_title'])
        jsonResponse = "{\"message\": \"Too Many Requests\", \"error\": 429}"  # current error message from reddit api
        url = urlStart + bookTitle + urlEnd
        print url
        while jsonResponse == "{\"message\": \"Too Many Requests\", \"error\": 429}":
            time.sleep(1)
            response = urllib.urlopen(url)
            jsonResponse = response.read()
        # print jsonResponse

        data = json.loads(jsonResponse)
        postArray = data["data"]["children"]  # gets to array of posts within the results
        numPosts = int(data["data"]["dist"])
        if numPosts > 10:
            numPosts = 10
        print numPosts
        for x in range(numPosts):
            postAuthor = postArray[x]["data"]["author"]
            postAuthor = postAuthor.encode("utf8")
            titleAndUrl = postArray[x]["data"]["title"] + "\n" + postArray[x]["data"]["url"]
            titleAndUrl = titleAndUrl.encode("utf8")
            csv_writer.writerow([row['\xef\xbb\xbfbook_id'], row['title'], row['isbn'], row['authors'], 'Reddit', postAuthor, titleAndUrl])
            # print postArray[x]["data"]["title"]  # title of post
            # print postArray[x]["data"]["url"]  # url of post
            # print postArray[x]["data"]["author"]  # author of post
        # test = test - 1
        # if test == 0:
        #    break

# book_id,title,isbn,author,review source,average rating,review author,review content
"""
with open("RedditResults.csv", mode='w') as csv_in:
    csv_writer = csv.writer(csv_in, delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['book_id', 'titles', 'isbn', 'author', 'review source', 'review author', 'review content'])

    postAuthors = [text.encode("utf8") for text in postAuthors]
    contents = [text.encode("utf8") for text in contents]

    index = 0
    contIndex = 0
    for pstnum in postAmounts:
        for i in range(pstnum):
            csv_writer.writerow([book_ids[index], titles[index], isbns[index], authors[index], 'Reddit', postAuthors[contIndex+i], contents[contIndex+i]])
        index = index + 1
        contIndex = contIndex + pstnum
"""