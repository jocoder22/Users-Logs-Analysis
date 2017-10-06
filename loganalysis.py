#!/usr/bin/env python
import psycopg2


# Connect to an existing database
def connect(database_name):
    """  Connect to the PostgreSQL database. Returns a database connection. """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        # THEN perhaps exit the program
        sys.exit(1)   # The easier method
        # OR perhaps throw an error
        raise e
        # If you choose to raise an exception,
        # It will need to be caught by the whoever called this function

database = "news"
db, cur = connect(database)
"""
create a view table: this creates a new  temporary table, articles2 that
updated the values in column slug to march those in path for
forming a join for our query later.
"""

articles2 = "create view articles2 as select author, title,\
concat('/article/', slug) as slug2 from articles; "
cur.execute(articles2)


""" Query the database to answer the first question: """
""" What is the most popular three articles of all time? """

query1 = "select a.title as article, count(*) as views from articles2 a,\
log b where a.slug2 = b.path group by b.path, a.title \
order by views desc limit 3; "

# pass query1 to the cursor to execute and store result as answer1
cur.execute(query1)
answer1 = cur.fetchall()
print 'The three most popular articles of all time are:'
for title, views in answer1:
    print '"{}" - {} views'.format(title, views)

print
print

""" Query the database again to answer the second question: """
""" Who is the most popular article author of all time? """

query2 = "select  a.name, count(a.name) as views from authors a, articles2 b, \
log c where a.id = b.author and b.slug2 = c.path group by a.name \
order by views desc;"

# pass query2 to the cursor to execute and return result
cur.execute(query2)
answer2 = cur.fetchall()
print 'The most popular article author of all time is:'
for name, views in answer2:
    print '"{}" - {} views'.format(name, views)

print
print

""" Query the database again to answer the third question: """
""" On which days did more than 1% of requests lead to errors? """
"""
create a view table logview: this creates a temporary table logview from the
log table with updated status column to having only the codes as code.
We use this view table to create other view tables below
"""
logview = "create view logview as select substring(status from 1 for 3) as \
code, to_char(time, 'FMMonth FMDD, YYYY') as day, count(path) as views from \
log group by code, day; "
cur.execute(logview)

"""
create another view table viewsum: this creates a temporary table to sum the
total visit to the sites each day from logview view table
"""
viewsum = "create view viewsum as select day, sum(views) as totalviews from \
logview group by day; "
cur.execute(viewsum)

"""
create a view table code400: this creates temporary table to select only the
subset from view table logview records of error requests  per day
"""

code400 = "create view code400 as select code, day, views from logview group \
by views, day, code having code != '200'; "
cur.execute(code400)

# using the two table views above to find the percentage

query3 = "select round(100.0 * (a.views / b.totalviews), 1) as percentage, \
a.day from code400 a, viewsum b where a.day = b.day \
order by percentage desc; "

# pass query3 to the cursor to execute and return result
cur.execute(query3)
answer3 = cur.fetchone()
print 'The day with more than 1% error request is:'
print '{0[1]} - {0[0]}% errors'.format(answer3)


# Close communication with the database
cur.close()
db.close()
