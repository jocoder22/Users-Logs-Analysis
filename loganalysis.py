# Python 2.7.12
import psycopg2

# Connect to an existing database
conn = psycopg2.connect("dbname=news")

# Open a cursor to perform database operations
cur = conn.cursor()

# create a view table: this creates a new  temporary table, articles2 that updated the values in column slug to march those in path for forming a join for our query later.

cur.execute("create view articles2 as select author, title, concat('/article/',slug) as slug2 from articles;")

# Query the database to answer the first question:
# What is the most popular three articles of all time?

query1 = "select a.title as article, count(b.path) as views from articles2 a, log b where a.slug2 = b.path group by b.path, a.title order by views desc limit 3;"

# pass query1 to the cursor to execute and store result as answer1
cur.execute(query1)
answer1 =  cur.fetchall()
print 'The three most popular articles of all time are:'
for i in range(len(answer1)):
	print '"{0[0]}" - {0[1]} views'.format(answer1[i])

print
print

# Query the database again to answer the second question:
# Who is the most popular article author of all time?

query2 = "select  a.name, count(a.name) as views from authors a, articles2 b, log c where a.id = b.author and b.slug2 = c.path group by a.name order by views desc;"

# pass query2 to the cursor to execute and return result
cur.execute(query2)
answer2 =  cur.fetchall()
print 'The most popular article author of all time is:'
for i in range(len(answer2)):
	print '"{0[0]}" - {0[1]} views'.format(answer2[i])

print
print

# Query the database again to answer the third question:
# On which days did more than 1% of requests lead to errors?
# create a view table logview: this creates a temporary table logview from the log table with updated status column to having only the codes as code. We use this view table to create other view tables below

cur.execute("create view logview as select substring(status from 1 for 3) as code, to_char(time, 'FMMonth DD, YYYY') as day, count(path) as views from log group by code, day;")

# create another view table viewsum: this creates a temporary table to sum the total visit to the sites each day from logview view table

cur.execute("create view viewsum as select day, sum(views) as totalviews from logview group by day;")


# create a view table code400: this creates temporary table to select only the subset from view table logview records of error requests  per day

cur.execute("create view code400 as select code, day, views from logview group by views, day, code having code != '200';")

# using the two table views above to find the percentage

query3 = "select round(100.0 * (a.views / b.totalviews), 1) as percentage, a.day from code400 a, viewsum b where a.day = b.day order by percentage desc limit 1;"

# pass query3 to the cursor to execute and return result
cur.execute(query3)
answer3 =  cur.fetchone()
print 'The day with more than 1% error request is:'
print '{0[1]} - {0[0]}% errors'.format(answer3)


# Close communication with the database
cur.close()
conn.close()
