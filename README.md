# Harry Potter fanfic data analysis


# 4
Create a database called fanfiction\_<lastname>. Create a stories\_orig table with url as the primary key. 

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

## a
Use \copy to load Fanfiction/stories\_orig.csv into the table. Despite what Postgres may say, the problem isn’t that url is the primary key; the problem is in the data. Explain. 

\copy stories_orig FROM data/stories_orig.csv CSV HEADER;

ERROR:  duplicate key value violates unique constraint "stories_orig_pkey"
DETAIL:  Key (url)=(http://www.fanfiction.net/s/9096319/1/Green-Eyed-Monster) already exists.

As the primary key, url has two constraints - the data must be unique, and cannot be null. The unique constraint is violated by the fact that the url for Green-Eyed-Monster is repeated, so there is a collision.

## b
Work around the data problem temporarily by adding a sequence column to the table, removing url as a primary key, and loading the table. (Consult the Postgres docs and/or StackOverflow.)

ALTER TABLE stories_orig DROP CONSTRAINT stories_orig_pkey;

\copy stories_orig FROM data/stories_orig.csv CSV HEADER;

ALTER TABLE stories_orig ADD COLUMN id SERIAL PRIMARY KEY;

## c
Fix the data problem using a select statement that joins stories\_orig with itself (!), checking for records with the same url. Try your sql with explain with and without an index, but run it with an index.

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

# 5
Write two python programs to fix the data problem. These are two strategies 

## a
One program sorts the rows of stories\_orig.csv and traverses rows in sorted order.

## b
The other program uses a hash:

### i
Find a way to map each row r to a number h(r) between 0 and N = 220-1. 
One suggestion (among many): represent published as mmddyy and words as nnn...n, and set h(r) to mmddyynnn...n mod N.

### ii
Create a python list of N empty lists.

### iii
Add each row r to the h(r)th list. 

### iv
Traverse the list of lists. If any list contains more than one row, compare them. 

## c
Which program runs faster? Explain