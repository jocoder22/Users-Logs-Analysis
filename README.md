# PURPOSE:
This purpose of this project is to analyze PostgreSQL database to reach business conclusion using an internal reporting tool. The internal reporting tool is a Python program using psycopg2 module to connect to the database.

# BACKGROUND:
The database is from a newspaper website. The database contains newspaper articles and web Sever log of activities on the site by readers. The log has a database row for each time a reader load a web page.

The database includes three tables vis:
  - The authors table which has information about the authors of articles
  - The articles table which has the articles themselves
  - The log table which has one entry each time a reader access the site

# PROJECT:
The project will build an internal reporting tool that uses information form the database to discover reader's activity and kinds of articles readers. This project will answer the following questions:

  1. What are the most popular three articles of all time?
      - this will report the three articles most viewed by readers.
  2. Who is the most popular article author of all time?
      - this will report the author who got the most articles viewed by readers adding together all articles written by each author
  3. The day with more than 1% of error requests?
      - The log table includes a column status that indicates the HTTP status code that the newspaper site sent to the site user's browse

 # CREATED VIEWS:
 In building this internal reporting tool I used views to query the database. Below are the commands used in creating the views. 

 #### VIEW articles2:
This creates view articles2 with modified the values in column slug in author table to march those in column path in log table for
forming a join for our queries later.

 `cur.execute("create view articles2 as select author, title, concat('/article/',slug) as slug2 from articles;")`


#### VIEW viewsum:
  This creates view viesum from the log table with column totalviews containing the total counts all request per day.
  
`cur.execute("create view viewsum as select date(time) as day, count(*) as totalviews from log group by day order by day;")`



 #### VIEW code400:
  This creates view code400 from the log table with column views containing only the counts of errors per day.

`cur.execute("create view code400 as select date(time) as day, count(*) as  views from log where status != '200 OK' group by day order by day;")`


# INTERNAL REPORTING TOOL:
The final internal reporting tool is the file, `loganalysis.py`

#### USING THE INTERNAL REPORTING TOOL:
This project makes use of the same Linux-based virtual machine (VM) as the preceding lessons.

If you have used an older version of this VM, you may need to install it into a new directory.

If you need to bring the virtual machine back online with `vagrant up`. Then log into it with `vagrant ssh`.

#### DOWNLOADING THE DATA
Next, [download the data here.](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) Next unzip this file after downloading. The file inside is called `newsdata.sql` and put this file into the vagrant directory, which is shared with your virtual machine.

Now load the newspaper site's data into your local database. To load the data, cd into the vagrant directory and use the command 
`psql -d news -f newsdata.sql`.
Here's what this command does:

- psql — the PostgreSQL command line program
- -d news — connect to the database named news which has been set up for you
- -f newsdata.sql — run the SQL statements in the file newsdata.sql

Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.
