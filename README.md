# Webscrape_Regression_IMDB

For this first project, a webscraper was created using Python and BeautifulSoup, to scrape movie data from IMDB. Regression analysis was done on this dataset to predict box office gross. Below are the main steps performed:

Since IMDB data was scattered across multiple pages for each movie, MySQL was chosen as the datastore (3NF) to store and do preliminary cleanup. To run this, create a new mysql database called 'imdb' and run [imdb_main](./scrape/imdb_main.py) after [changing mysql user info](https://github.com/ngovindaraj/Webscrape_Regression_IMDB/blob/master/scrape/sql_db.py#L87-L90).

Below are the jupyter notebooks for analysis:
- [BeautifulSoup code for scraping one movie](./1_imdb_webscrape.ipynb)
- [Raw scraped dataset](./imdb_df_raw.csv)
- [EDA ipynb](./2_imdb_cleanup.ipynb)
- [Linear Regression ipynb](./3_imdb_regression_LR.ipynb)
- [RandomForest Regression ipynb](./4_imdb_regression_RF.ipynb)
