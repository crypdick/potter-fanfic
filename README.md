# Harry Potter fanfic data analysis


# 4
Create a database called fanfiction\_<lastname>. Create a stories\_orig table with url as the primary key. 

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
Which program runs faster? Explain.