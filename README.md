# PURPOSE:
This purpose of this project is to analyze PostgreSQL database to reach business conclusion using an internal using tool. The internal reporting tool is a Python program using the psycopg2 module to connect to the database.

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
  This creates the view articles2 that updated the values in column slug to march those in path for forming a join for our query later.

 `cur.execute("create view articles2 as select author, title, concat('/article/',slug) as slug2 from articles;")`



#### VIEW logview:
  This creates the view logview from the log table with updated status column to having only the codes as code. We use this view table to create other view tables below

 `cur.execute("create view logview as select substring(status from 1 for 3) as code, to_char(time, 'FMMonth DD, YYYY') as day, count(path) as views from log group by code, day;")`



 #### VIEW viewsum:
  This creates a temporary table viewsum to sum the total visits to the sites each day from logview view table

 `cur.execute("create view viewsum as select day, sum(views) as totalviews from logview group by day;")`



 #### VIEW code400:
  This creates the view to select only the subset from view table logview records of error requests  per day

 `cur.execute("create view code400 as select code, day, views from logview group by views, day, code having code != '200';")`



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
