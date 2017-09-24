# Harry Potter fanfic data analysis


# 4
Create a database called fanfiction\_<lastname>. Create a stories\_orig table with url as the primary key. 

CREATE DATABASE fanfiction_duffrindecal;
\connect fanfiction_duffrindecal

CREATE TABLE storied_orig (
  seq_id  serial primary key,
  hubway_id   bigint,
  status  character varying(10),
  duration  integer,
  start_date  timestamp without time zone,
  strt_statn  integer,
  end_date  timestamp without time zone,
  end_statn   integer,
  bike_nr   character varying(20),
  subsc_type  character varying(20),
  zip_code  character varying(6),
  birth_date  integer,
  gender  character varying(10));

## a
Use \copy to load Fanfiction/stories\_orig.csv into the table. Despite what Postgres may say, the problem isn’t that url is the primary key; the problem is in the data. Explain. 

## b
Work around the data problem temporarily by adding a sequence column to the table, removing url as a primary key, and loading the table. (Consult the Postgres docs and/or StackOverflow.)

## c
Fix the data problem using a select statement that joins stories\_orig with itself (!), checking for records with the same url. Try your sql with explain with and without an index, but run it with an index.

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