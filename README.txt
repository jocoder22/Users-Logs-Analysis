PURPOSE:
This purpose of this project is to analyze PostgreSQL database to reach business conclusion using an internal using tool. The internal reporting tool is a Python program using the psycopg2 module to connect to the database.

BACKGROUND:
The database is from a newspaper website. The database contains newspaper articles and web Sever log of activities on the site by readers. The log has a database row for each time a reader load a web page.

The database includes three tables vis:
  -- The authors table which has information about the authors of articles
  -- The articles table which has the articles themselves
  -- The log table which has one entry each time a reader access the site

PROJECT:
The project will build an internal reporting tool that uses information form the database to discover reader's activity and kinds of articles readers. This project will answer the following questions:
a. what are the most popular three articles of all time?
 --- this will report the three articles most viewed by readers.
b. Who is the most popular article author of all time?
 --- this will report the author who got the most articles viewed by readers when you sum all articles by each author
c. The day with more than 1% of requests lead to error?
 --- The log table includes a column status that indicates the HTTP status code that the newspaper site sent to the site user's browse

 CREATED VIEWS:
 In building this internal reporting tool, I added views to the database. Below are the commands used in creating the views. They commands/codes are include in the python file used for the project.

 VIEW articles2:
  This creates a temporary table, articles2 that updated the values in column slug to march those in path for forming a join for our query later.

 cur.execute("create view articles2 as select author, title, concat('/article/',slug) as slug2 from articles;")



VIEW logview:
  This creates a temporary table logview from the log table with updated status column to having only the codes as code. We use this view table to create other view tables below

 cur.execute("create view logview as select substring(status from 1 for 3) as code, to_char(time, 'FMMonth DD, YYYY') as day, count(path) as views from log group by code, day;")



 VIEW viewsum:
  This creates a temporary table viewsum to sum the total visits to the sites each day from logview view table

 cur.execute("create view viewsum as select day, sum(views) as totalviews from logview group by day;")



 VIEW code400:
  This creates temporary table to select only the subset from view table logview records of error requests  per day

 cur.execute("create view code400 as select code, day, views from logview group by views, day, code having code != '200';")



INTERNAL REPORTING TOOL:
The final internal reporting tool is the file, loganalysis.py
