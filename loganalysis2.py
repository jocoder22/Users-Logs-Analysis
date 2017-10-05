#!/usr/bin/env python
import psycopg2

"""
create a view table: this creates a new  temporary table, articles2 that
updated the values in column slug to march those in path for
forming a join for our query later.
"""

articles2 = "create view articles2 as select author, title,\
concat('/article/', slug) as slug2 from articles; "
cur.execute(articles2)


# Query the database to answer the first question:
# What is the most popular three articles of all time?

query1 = "select a.title as article, count(*) as views from articles2 a,\
log b where a.slug2 = b.path group by b.path, a.title \
order by views desc limit 3; "

# Query the database again to answer the second question:
# Who is the most popular article author of all time?

query2 = "select  a.name, count(*) as views from authors a, articles2 b, \
log c where a.id = b.author and b.slug2 = c.path group by a.name \
order by views desc;"


# Query the database again to answer the third question:
# On which days did more than 1% of requests lead to errors?
"""

logview = "create view logview as select substring(status from 1 for 3) as \
code, to_char(time, 'FMMonth FMDD, YYYY') as day, count(path) as views from \
log group by code, day; "
cur.execute(logview)


create another view viewsum: this creates a view to sum the
total visit to the sites each day from logview view table

viewsum = "create view viewsum as select day, sum(views) as totalviews from \
logview group by day; "

viewsum = "create view viewsum as select date(time) as day, count (*) as \
totalviews from log group by day; "

"""
# cur.execute(viewsum)

"""
create a view table code400: this creates temporary table to select only the
subset from view table logview records of error requests  per day


code400 = "create view code400 as select code, day, views from logview group \
by views, day, code having code != '200'; "

code400 = "create view code400 as select date(time) as day, count(*) as views \
from log group by day, status having status != '200 OK'; "
"""
# cur.execute(code400)

# using the two table views above to find the percentage


viewsum = "create view viewsum as select date(time) as day, count(*) as \
totalviews from log group by day; "

code400 = "create view code400 as select date(time) as day, count(*) as views \
from log where status != '200 OK' group by day; "

query3 = "select round(100.0 * (a.views / b.totalviews), 1) as percentage, \
to_char(a.day, 'FMMonth FMDD, YYYY') as d_day from code400 a, viewsum b where \
a.day = b.day order by percentage desc limit 1; "


# Connect to an existing database
def connect(database_name):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        # THEN perhaps exit the program
        sys.exit(1) # The easier method
        # OR perhaps throw an error
        raise e
        # If you choose to raise an exception,
        # It will need to be caught by the whoever called this function


def fetch_query(query):
    “””
    Connect to the database, query, fetch results, close connection, return results
    “””
    # connect to database, grab cursor
    db, c = connect(db_name="news")
    # execute
    c.execute(query)
    result = c.fetchall()
    # commit
    # close
    c.close()
    db.close()
    # return results
    return result



def print_results(results, label):
    “””
    Prints the results of a query, appends the label (errors or views)
    “””
    for name, count in results:
        print '"{}" - {} {}'.format(name, count, label)

def print_top_articles():
    “””
    Fetch top articles using helper function, print results using helper
    “””
    return print_results(fetch_query(query1), 'views')


def print_top_authors():
    “””
    Fetch top authors using helper function, print results using helper
    “””
    return print_results(fetch_query(query2), 'views')


def print_top_error_days():
    “””
    Fetch top error days using helper function, print results using helper
    “””
    fetch_query(viewsum)
    fetch_query(code400)
    return print_results(fetch_query(query3), 'errors')


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()
