# Harry Potter fanfic data analysis

## Creating db, setting URL as primary key

    CREATE DATABASE fanfiction_duffrindecal;
    \connect fanfiction_duffrindecal
    
    CREATE TABLE stories_orig (
      RATING  varchar(2),
      UPDATED   timestamp without time zone,
      FAVORITES  integer,
      STARRINGCHARS  text,
      CHAPTERS  integer,
      COMPLETE  bool,
      COLLECTEDINFO  text,
      GENRE   text,
      DESCRIPTION   text,
      LANGUAGE  text,
      AUTHOR  text,
      URL  text primary key,
      FOLLOWS  integer,
      TITLE  text,
      REVIEWS  integer,
      PUBLISHED  timestamp without time zone,
      WORDS  integer);

### a. Reading in CSV data


    \copy stories_orig FROM data/stories_orig.csv CSV HEADER;
    
    ERROR:  duplicate key value violates unique constraint "stories_orig_pkey"
    DETAIL:  Key (url)=(http://www.fanfiction.net/s/9096319/1/Green-Eyed-Monster) already exists.

Primary keys have two constrains: the value must not be NULL and it must be unique. The problem is we apparently have duplicate entries, so SQL helpfully does not let us load in the data.

### b. Temporary workaround: removing constraints

    ALTER TABLE stories_orig DROP CONSTRAINT stories_orig_pkey;

    \copy stories_orig FROM data/stories_orig.csv CSV HEADER;

    ALTER TABLE stories_orig ADD COLUMN id SERIAL PRIMARY KEY;

### c. Removing duplicates

We joined the table with itself, checking for records with the same URL. We compared the join statement with and without an index using the `EXPLAIN` commands.

    EXPLAIN SELECT * FROM stories_orig AS a JOIN stories_orig AS b ON a.url = b.url WHERE a.id < b.id;
    
                                         QUERY PLAN                                      
    -------------------------------------------------------------------------------------
     Hash Join  (cost=93285.36..266784.12 rows=204568 width=978)
       Hash Cond: (a.url = b.url)
       Join Filter: (a.id < b.id)
       ->  Seq Scan on stories_orig a  (cost=0.00..46658.05 rows=613705 width=489)
       ->  Hash  (cost=46658.05..46658.05 rows=613705 width=489)
             ->  Seq Scan on stories_orig b  (cost=0.00..46658.05 rows=613705 width=489)
    (6 rows)
    
With an index:

    CREATE INDEX ON stories_orig (url); 
    
    EXPLAIN SELECT * FROM stories_orig AS a JOIN stories_orig AS b ON a.url = b.url WHERE a.id < b.id;
                                                     QUERY PLAN                                                  
    -------------------------------------------------------------------------------------------------------------
     Merge Join  (cost=1.10..220057.11 rows=204568 width=978)
       Merge Cond: (a.url = b.url)
       Join Filter: (a.id < b.id)
       ->  Index Scan using stories_orig_url_idx on stories_orig a  (cost=0.55..104658.64 rows=613705 width=489)
       ->  Index Scan using stories_orig_url_idx on stories_orig b  (cost=0.55..104658.64 rows=613705 width=489)
    (5 rows)

Adding the index greatly reduces the time to join the tables because it replaces the hashing step with an index scan.


## Fixing the data

### Strategy 1: Sorting the rows of stories\_orig.csv and traversing rows in sorted order.

### Strategy 2: Hashing

#### Hash1: Map each row r to a number h(r) between 0 and N = 2^20-1. 
One suggestion (among many): represent published as mmddyy and words as nnn...n, and set h(r) to mmddyynnn...n mod N.

#### Hash2: Create a python list of N empty lists.

#### Hash3: Add each row r to the h(r)th list. 

#### Hash4: Traverse the list of lists. If any list contains more than one row, compare them. 

### Comparison of munging strategies