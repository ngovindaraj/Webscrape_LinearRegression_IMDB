import itertools
import mysql.connector as sqlConn
import pandas as pd

#Remove $ and comma from currency handle abbreviations and convert to int($1.2M -> 1200000)
def currency_str_to_int(amt):
    if isinstance(amt, str):
        amt = amt.replace('$','').replace(',','')
        if amt[-1] == 'M':
            amt = float(amt.replace('M',''))*10**6
    return int(amt)


def read_imdb_sql_table():
    conn = sqlConn.connect(user='ngovindaraj', password ='abcd', database='imdb', host='localhost')
    imdb_df = pd.read_sql_query('''
    SELECT mv.movie_id AS id, mv.movie_title AS title, mv.genre AS genre, mv.runtime AS runtime, mv.release_dt AS release_dt, 
           mon.budget AS budget, mon.us_boxoffice_gross AS us_boxoffice_gross,
           r.mpaa_rating AS mpaa_rating, r.user_rating AS user_rating, r.total_votes AS total_votes, r.critic_score AS critic_score
    FROM movie as mv, money as mon, people as p, rating as r 
    WHERE mv.movie_id = p.movie_id AND mv.movie_id = mon.movie_id AND mv.movie_id=r.movie_id;
    ''', conn)
    conn.disconnect()
    return imdb_df
