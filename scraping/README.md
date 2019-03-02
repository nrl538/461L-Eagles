# Documentation for the GoodReads scraper

### Tools used

Our goodreads scraper is using selenium for dynamic web content scraping
and for logging in our scrape user.

We also use Pandas for ease of converting between scraped data and csv
via dataframes.


### Procedure
  1. Scraper calls `sign_in('SCRAPE_USER_NAME', 'SCRAPE_PASS_WORD')` to
     log our scrape user in.
  2. Using our list of books to scrape (which is limited to 13 and
     hardcoded for phase 1), we search for the book and click on it in
     the search results page of GoodReads.
  3. We then grab the cover image link, description, authors, metadata,
     details, and purchase link.
  4. We dump all of this data into a csv file named `book_data.csv`
