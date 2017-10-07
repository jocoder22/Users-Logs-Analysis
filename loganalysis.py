#!/usr/bin/env python
import psycopg2


# Connect to an existing database
def connect(database_name):
    """Connect to the PostgreSQL database.
        Returns a database connection.
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        # THEN perhaps exit the program
        sys.exit(1)  # The easier method
        # OR perhaps throw an error
        # raise e
        # If you choose to raise an exception,
        # It will need to be caught by the whoever called this function

database = 'news'

"""
create a view articles2: this creates view articles2 with modified the values
in column slug in author table to march those in column path in log table for
forming a join for our queries later.
"""
query1 = "create view articles2 as select author, title, \
concat('/article/',slug) as slug2 from articles;"

""" Query the database to answer the first question: """
""" What is the most popular three articles of all time? """
query2 = "select a.title as article, count(b.path) as views from articles2 a, \
log b where a.slug2 = b.path group by b.path, a.title order by views  desc \
limit 3;"

""" Query the database again to answer the second question: """
""" Who is the most popular article author of all time? """
query3 = "select  a.name, count(a.name) as views from authors a, articles2 b, \
log c where a.id = b.author and b.slug2 = c.path group by a.name order by \
views desc;"

""" Query the database again to answer the third question: """
""" On which days did more than 1% of requests lead to errors? """
"""
create a view viewsum: this creates view viesum from the log table with column
totalviews having the total counts all request per day.
"""
query4 = "create view viewsum as select date(time) as day, count(*) as  \
totalviews from log group by day order by day;"

"""
create a view code400: this creates view code400 from the log table with column
views having only the counts of errors per day.
"""

query5 = "create view code400 as select date(time) as day, count(*) as  views \
from log where status != '200 OK' group by day order by day;"


# using the two table views above to find the percentage

query6 = "select to_char(a.day, 'FMMonth FMDD, YYYY') as dayy, \
round(100.0 * (a.views::numeric / b.totalviews), 1) as percentage from \
code400 a, viewsum b where a.day = b.day order by percentage desc limit 1;"


def fetch_query(query, cur):
    """
    Connect to the cursor, query, fetch results, return results
    """
    # execute
    cur.execute(query)
    dbresult = cur.fetchall()
    # return results
    return dbresult


def print_results(tablel, label):
    """
    Add space before result to make for easy reading and print out the results
    with label added.
    """
    print  # just space
    print  # another space
    print  # another space
    for val1, val2 in tablel:
        print '{} - {} {}'.format(val1, val2, label)


def print_top_articles():
    """
    Connect to database, grap cursor, fetch top articles using helper function,
    print results using helper, close cursor and database.
    """
    db, c = connect(database)
    c.execute(query1)
    tablell = fetch_query(query2, c)
    print_results(tablell, "views")
    c.close()
    db.close()


def print_top_authors():
    """
    Connect to database, grap cursor, fetch top authors using helper function,
    print results using helper, close cursor and database.
    """
    db, c = connect(database)
    c.execute(query1)
    tablell = fetch_query(query3, c)
    print_results(tablell, "views")
    c.close()
    db.close()


def print_top_error_days():
    """
    Connect to database, grap cursor, error days using helper function
    print results appropriately, close cursor and database.
    """
    db, c = connect(database)
    c.execute(query4)
    c.execute(query5)
    tablell = fetch_query(query6, c)
    print
    print
    print
    for day, percentage in tablell:
        print '{} - {}%'.format(day, percentage)
    c.close()
    db.close()


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()
