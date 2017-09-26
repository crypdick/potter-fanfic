import time
import pandas as pd

with open('data/stories_orig.csv', 'r') as file:
	stories_a = file.read()

stories_b = stories_a

#5A
#One program sorts the rows of stories_orig.csv and traverses rows in sorted order.

stories_a = pd.read_csv('data/stories_orig.csv')

start_time = time.time()

stories_a = stories_a.sort_values(by='URL')

previous_url = ''
for i in stories_a.index:
	current_url = stories_a.loc[i, 'URL']
	if current_url == previous_url:
		stories_a.drop(i, inplace=True)
	previous_url = current_url

#save file

time_elapsed = time.time() - start_time

print('5A: ' + time_elapsed)

#5B
#The other program uses a hash:
#Find a way to map each row r to a number h(r) between 0 and N = 2^20-1. 
#One suggestion (among many): represent published as mmddyy and words as nnn...n, and set h(r) to mmddyynnn...n mod N.
#Create a python list of N empty lists.
#Add each row r to the h(r)th list. 
#Traverse the list of lists. If any list contains more than one row, compare them. 

stories_b = pd.read('data/stories_orig.csv')

hash_table = [[] for i in range(2**20)]

def hash_function(date, url):
	hashed_index = 0
	if type(date) == type('08-25-1999'):
		hashed_index = int(date.replace('-', ''))
	for character in url:
		hashed_index += ord(character) # multiply by index
	return hashed_index % (2**20)

start_time = time.time()

for row in stories_b.iterrows():
	date, url = row[1][['PUBLISHED', 'URL']]
	hashed_index = hash_function(date, url)
	hash_table[hashed_index].append(row[1])

#for rows in stories_b.iterrows():
	#date, url = stories_b.ix[i, ['PUBLISHED', 'URL']]
	#hashed_index = hash_function(date, url)
	#hash_table[hashed_index].append(stories_b.loc[i])

for hash_table_index in range(len(hash_table)):
	print(hash_table[hash_table_index])
	if len(hash_table[hash_table_index]) > 1:
		urls = []
		print(type(hash_table[hash_table_index]))
		for sublist_index in range(len(hash_table[hash_table_index])):
			print(hash_table[hash_table_index[sublist_index]])
			if hash_table[hash_table_index[sublist_index]]['URL'] in urls:
				del hash_table[hash_table_index[sublist_index]]
			else:
				urls.append(hash_table[hash_table_index[sublist_index]]['URL'])
	#if type(0) = type(hash_table[hashed_index]):
	#	hash_table[hash_index] = stories_b.loc[i]
	#if current_url == previous_url:
#		stories_a.drop(i, inplace=True)
#	previous_url = current_url


#save file

time_elapsed = time.time() - start_time

print('5B: ' + time_elapsed)

#5C
#Which program runs faster? Explain