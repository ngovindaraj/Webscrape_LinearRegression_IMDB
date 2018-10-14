# SQL Interface for IMDB movie data.

import mysql.connector
from mysql.connector import Error


class MySql(object):
    cnx_ = None
    cursor_ = None
    host_ = None
    user_ = None
    passwd_ = None
    db_ = None

    def __init__(self, host='localhost', user='', passwd='', db=''):
        self.host_ = host
        self.user_ = user
        self.passwd_ = passwd
        self.db_ = db

    def __del__(self):
        self.cnx_.close()

    def sqlExecute(self, execStr, toPrint):
        if toPrint:
            print(execStr)
        try:
            self.cursor_.execute(execStr)
        except mysql.connector.Error as err:
            print(err.msg)
            return False
        return True

    def sqlSelect(self, tabName, colNames, whereCond, toPrint=False):
        execStr = 'SELECT {col} FROM {table} WHERE {cond}'.format(
            col=colNames, table=tabName, cond=whereCond)
        try:
            self.sqlExecute(execStr, toPrint)
            ret = self.cursor_.fetchall()  # fetch answers
            return ret
        except mysql.connector.Error as err:
            print(err.msg)
            return None

    # Update a single column in a table based on where clause
    def sqlUpdate(self, tabName, colName, colVal, whereCond, toPrint=False):
        execStr = 'UPDATE {table} SET {cN}="{cV}" WHERE {cond}'.format(
            table=tabName, cN=colName, cV=colVal, cond=whereCond)
        try:
            self.sqlExecute(execStr, toPrint)
            self.cnx_.commit()
        except mysql.connector.Error as err:
            print(err.msg)

    # Connect to MySQL Database
    def connect(self):
        self.cnx_ = mysql.connector.connect(
            host=self.host_,
            database=self.db_,
            user=self.user_,
            password=self.passwd_)
        if self.cnx_.is_connected():
            self.cursor_ = self.cnx_.cursor()

    # Create tables
    def createTable(self, tabName, colList, toPrint=False):
        colListStr = ',\n\t'.join(colList)
        execStr = 'CREATE TABLE IF NOT EXISTS %s (\n\t%s\n);' % (tabName,
                                                                 colListStr)
        return self.sqlExecute(execStr, toPrint)

    def insertRow(self, tabName, colList, colFmtStr, valList, toPrint=False):
        query = 'INSERT INTO {} ({}) VALUES({})'.format(
            tabName, colList, colFmtStr)
        try:
            self.cursor_.executemany(query, valList)
            self.cnx_.commit()
        except mysql.connector.Error as err:
            print(err.msg)
            return False
        return True


name_id_ctr = 0


def create_mysql_connection():
    sql = MySql(user='ngovindaraj', passwd='the rock', db='imdb')
    sql.connect()
    return sql


def create_imdb_tables(sql):
    sql.createTable('movie', [
        'movie_id int PRIMARY KEY NOT NULL',
        'movie_title varchar(100) NOT NULL', 'genre varchar(100) NOT NULL',
        'runtime int NOT NULL', 'release_dt varchar(100) DEFAULT NULL'
    ])

    sql.createTable('rating', [
        'movie_id int PRIMARY KEY NOT NULL',
        'mpaa_rating varchar(100) NOT NULL', 'user_rating float NOT NULL',
        'total_votes bigint NOT NULL', 'critic_score int NOT NULL'
    ])

    sql.createTable('money', [
        'movie_id int PRIMARY KEY NOT NULL', 'budget varchar(100) NOT NULL',
        'us_boxoffice_gross varchar(200) NOT NULL'
    ])

    sql.createTable('people', [
        'movie_id int PRIMARY KEY NOT NULL', 'director_id int NOT NULL',
        'writer1_id int NOT NULL', 'writer2_id int NOT NULL',
        'actor1_id int NOT NULL', 'actor2_id int NOT NULL',
        'actor3_id int NOT NULL'
    ])

    sql.createTable(
        'names',
        ['name_id int PRIMARY KEY NOT NULL', 'names varchar(200) NOT NULL'])


def insert_imdb_movie(sql, row_tuple):
    return sql.insertRow("movie",
                         'movie_id, movie_title, genre, runtime, release_dt',
                         '%s, %s, %s, %s, %s', [row_tuple])


def insert_imdb_rating(sql, row_tuple):
    return sql.insertRow(
        "rating",
        'movie_id, mpaa_rating, user_rating, total_votes, critic_score',
        '%s, %s, %s, %s, %s', [row_tuple])


def insert_imdb_money(sql, row_tuple):
    return sql.insertRow("money", 'movie_id, budget, us_boxoffice_gross',
                         '%s, %s, %s', [row_tuple])


def insert_imdb_people(sql, row_tuple):
    return sql.insertRow(
        "people",
        'movie_id, director_id, writer1_id, writer2_id, actor1_id, actor2_id, actor3_id',
        '%s, %s, %s, %s, %s, %s, %s', [row_tuple])


def insert_imdb_name(sql, row_tuple):
    return sql.insertRow("names", 'name_id, names', '%s, %s', [row_tuple])


# Given a name, get corresponding name_id from 'names' table
# if name is already found, just 'select' the name_id
# if name is not found, insert name/name_id and return name_id
def populateName(sql, nameStr):
    global name_id_ctr
    name_id = sql.sqlSelect('names', 'name_id', 'names="{}"'.format(nameStr))
    if not name_id:
        insert_imdb_name(sql, (name_id_ctr, nameStr))
        name_id = name_id_ctr
        name_id_ctr += 1
        return name_id
    else:
        return name_id[0][0]  # To get value inside list of tuples


# Test code
# sql = create_mysql_connection()
# sql.sqlUpdate('money', 'us_boxoffice_gross', 'hi3', 'movie_id=10000')
# insert_imdb_movie(sql, (1, 'abc', 'A', 10, '1994-05-10'))
# insert_imdb_rating(sql, (2, 'efg', 10.0, 20, 10))
# insert_imdb_money(sql, (2, 'efg', 'B'))
# insert_imdb_people(sql, (2, 10, 20, 30, 40, 50, 60))
# print(populateName(sql, 'efg'))
# print('Done')
