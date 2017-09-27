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


    \copy stories_orig FROM data/stories_orig.csv CSV HEADER
    
    ERROR:  duplicate key value violates unique constraint "stories_orig_pkey"
    DETAIL:  Key (url)=(http://www.fanfiction.net/s/9096319/1/Green-Eyed-Monster) already exists.

Primary keys have two constrains: the value must not be NULL and it must be unique. The problem is we apparently have duplicate entries, so SQL helpfully does not let us load in the data.

### b. Temporary workaround: removing constraints

    ALTER TABLE stories_orig DROP CONSTRAINT stories_orig_pkey;

    \copy stories_orig FROM stories_orig.csv CSV HEADER

    ALTER TABLE stories_orig ADD COLUMN id SERIAL PRIMARY KEY;

### c. Removing duplicates

We joined the table with itself, checking for records with the same URL. We compared the join statement with and without indexing URLs using the `EXPLAIN` commands.

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
    
With a URL index:

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


Adding the stories_orig_url_idx index greatly reduces the time to join the tables (from 46658 to 1.10) because it replaces the hashing step with an index scan.


## Fixing the data

### Strategy 1: Sorting the rows of stories\_orig.csv and traversing rows in sorted order.

### Strategy 2: Hashing

1. Map each row r to a number h(r) between 0 and N = 2^20-1. 

2. Create a python list of N empty lists.

3. Add each row r to the h(r)th list. 

4. Traverse the list of lists. If any list contains more than one row, compare them. 

### Comparison of munging strategies

We expect the sort and traverse strategy to have O(N log N) complexity. First, the rows are sorted with quicksort, which is N log N on average. Then, we go through the list from top to bottom looking for duplicate rows, which is N operations. The N + Nlog N operations asymptotically converse to O(NlogN).

We expect the hashing strategy to be O(N). First, for every row we compute the hash and insert the data into a table, which is O(N). Then, we go through the table looking for rows with length > 1, which is O(P) (where P is the length of our hash table, in our case about 1,050,000 or ~2N). If we find such a list, we should in principle have a much smaller list to deduplicate. Thus, our algorithm should have a complexity of 3N, or simply O(N) magnitude.

Thus, we expect the hash to be slightly faster than the hash function. However, the hashing function was much slower than strategy 1. The sort and traverse strategy took 15.05 seconds to deduplicate the table. In contrast, deduplicating the hash table took 460 seconds!

There most likely culprit is the overhead from using Pandas to manage our csv data. Iterating through the dataframe is costly, since it has to generate a pd.Series object at each iteration. Then, we extract the url and date from each Series object by the column label in `date, url = row[['PUBLISHED', 'URL']]`. Later, when finding duplicate URLs, we are once again searching each pd.Series using keyword searches. 

In addition, we may just be getting unlucky with the entries clustering in our hash table due to hash collisions. This would cause us to have to make more comparisons.

A faster alternative that avoids Panda's overhead would have been to use the built-in Python CSV reader and its DictReader method to [generate dictionaries](https://stackoverflow.com/a/26881921/4212158) to store in our hash table.