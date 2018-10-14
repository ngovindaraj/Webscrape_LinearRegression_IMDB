# Webscrape_LinearRegression_IMDB

For this first project, a webscraper was created using Python and BeautifulSoup, to scrape movie data from IMDB. Regression analysis was done on this dataset to predict box office gross. Below are the main steps performed:

Since IMDB data was scattered across multiple pages for each movie, MySQL was chosen as the datastore (3NF) to store and do preliminary cleanup. To run this, create a new mysql database called 'imdb' and run [imdb_main](./scrape/imdb_main.py) after changing mysql user info.

Below are the jupyter notebooks for analysis:
- [BeautifulSoup code for scraping one movie](./1_imdb_webscrape.ipynb)
- [Raw scraped dataset](https://github.com/ngovindaraj/P1_IMDB_WebScrape/blob/master/imdb_df_raw.csv)
- [EDA ipynb](https://github.com/ngovindaraj/P1_IMDB_WebScrape/blob/master/imdb_cleanup.ipynb)
- [Prediction ipynb](https://github.com/ngovindaraj/P1_IMDB_WebScrape/blob/master/imdb_regression.ipynb)
