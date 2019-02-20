# Github Repo for the Eagles team (461L S19)

### Current teams - Phase 1

- Eric & Nabil: Backend
- Nelson & Hiep: Scraper
- Wesley & Michael: Front end/Tests

### Deliverables - Phase 1
- 13 static web pages each with contents of a different book
- 1 static home page
- Basic scraper with documentation
- Unit tests for scraper

### Details - Phase 1

- Design and document the scraper and webapp
- Add 14 static web pages that display data from specified in the use cases i.e. titles, book covers, ratings, reviews
- Learn Python and Flask
- Build basic scraping script and collect aggregated percentage based star rating for 14 books


### Goals - Phase 1

- 13 Static web pages each for a different book. Each web page will have the book’s cover, author, title, short description, at least one link to purchase, and at least one basic review. This review will not yet be based on overall internet sentiment.
- 1 Static Homepage with a background and search bar. Search functionality includes searching by author or title only.
- One Flask server integrated with MySQL, and test various endpoints with Postman. The flask server should have login/logout functionality, routes to all static pages mentioned above, and should fill in the static web page templates with book data.
- One scraper that pulls book data only from Goodreads. The scraper should pull book titles, authors, basic description, at least one simple rating, and the book cover picture. The link to purchase each book will be pulled by hand for now. This review/rating will not yet be based on overall internet sentiment.
- Unit tests and documentation for the scraper
