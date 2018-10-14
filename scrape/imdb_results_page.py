'''
Parse one IMDB movie results page.
Note: for this project use only US English language movies
List of fields expected for each result:
- Movie title     - String
- MPAA rating     - Enum
- Metascore  /100 - Float
- User Rating /10 - Float
- Genre           - Enum
- Runtime in mins - Int
- *Director       - Enum
- *Stars          - List of Enum
- US Gross        - Int
- #Votes          - Int
'''

# import libraries
import re
from utils import readURL, html2Soup, getTagText, getInt, getFloat
from imdb_movie_page import process_one_movie_url
from sql_db import (create_mysql_connection, insert_imdb_movie,
                    insert_imdb_rating, insert_imdb_money, insert_imdb_people,
                    populateName)


def insert_one_movie_into_mysql(
        sql, sno, title, mpaa_rating, metascore, user_rating, genre, runtime,
        votes_count, us_box_gross, director, star1, star2, star3, movie_url,
        budget, release_dt, writer1, writer2):
    director_id = populateName(sql, director)
    star1_id = populateName(sql, star1)
    star2_id = populateName(sql, star2)
    star3_id = populateName(sql, star3)
    writer1_id = populateName(sql, writer1)
    writer2_id = populateName(sql, writer2)
    insert_imdb_movie(sql, (sno, title, genre, runtime, release_dt))
    insert_imdb_rating(sql, (sno, mpaa_rating, user_rating, votes_count,
                             metascore))
    insert_imdb_money(sql, (sno, budget, us_box_gross))
    insert_imdb_people(sql, (sno, director_id, writer1_id, writer2_id,
                             star1_id, star2_id, star3_id))


def get_votes(mv):
    try:
        votes = getTagText(mv.find("p", class_="sort-num_votes-visible"))
        votes_count = 0
        if votes is not 'Empty':
            votes_count = getInt(votes.split()[1].replace(',', ''))
        return votes_count
    except (IndexError, ValueError):
        return 0


def get_user_rating(mv):
    user_rating = mv.find("div", class_="inline-block ratings-imdb-rating")
    user_rating_num = 0
    if user_rating is not None:
        user_rating_num = getFloat(getTagText(user_rating.find("strong")))
    return user_rating_num


def get_us_box_gross(mv):
    try:
        return getTagText(
            mv.find("p", class_="sort-num_votes-visible")).split()[-1]
    except IndexError:
        return 'Empty'


# For each movie use BeautifulSoup find() to get all the relevant fields.
# After processing one movie, insert it to MySQL
def process_results_one_movie(sql, mv):
    sno = getInt(
        getTagText(
            mv.find("span", class_="lister-item-index unbold text-primary")))
    title = getTagText(mv.find("h3", class_="lister-item-header").find("a"))
    mpaa_rating = getTagText(mv.find("span", class_="certificate"))
    metascore = getInt(getTagText(mv.find("span", class_="metascore")))
    user_rating = get_user_rating(mv)
    genre = getTagText(mv.find("span", class_="genre"))
    runtime = getTagText(mv.find("span", class_="runtime"))
    runtimeNum = getInt(runtime.split()[0])
    votes_count = get_votes(mv)
    us_box_gross = get_us_box_gross(mv)
    director = getTagText(mv.find('a', href=re.compile('adv_li_dr_0')))
    star1 = getTagText(mv.find('a', href=re.compile('adv_li_st_0')))
    star2 = getTagText(mv.find('a', href=re.compile('adv_li_st_1')))
    star3 = getTagText(mv.find('a', href=re.compile('adv_li_st_2')))
    movie_url = mv.find('a', href=re.compile('/title/'))['href']
    budget, release_dt, writer1, writer2 = process_one_movie_url(movie_url)
    budget, release_dt, writer1, writer2 = '', '', '', ''
    insert_one_movie_into_mysql(
        sql, sno, title, mpaa_rating, metascore, user_rating, genre,
        runtimeNum, votes_count, us_box_gross, director, star1, star2, star3,
        movie_url, budget, release_dt, writer1, writer2)
    cond = 'movie_id={}'.format((sno))
    sql.sqlUpdate('money', 'us_boxoffice_gross', us_box_gross, cond)


def process_results_page(sql, url):
    html = readURL(url)
    main_section = html2Soup(html).find(id="main")
    for each_movie in main_section.select(".article .lister-item-content"):
        process_results_one_movie(sql, each_movie)


# test
# sql = create_mysql_connection()
# process_results_page(sql, '/Users/navina/Desktop/test.html')
