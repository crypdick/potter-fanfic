import time
import pandas as pd
#
# with open('data/stories_orig.csv', 'r') as file:
#     stories_a = file.read()

# FIRST IMPLEMENTATION: sorts the rows traverses rows in sorted order.

stories_a = pd.read_csv('data/stories_orig.csv')

start_time = time.time()

stories_a = stories_a.sort_values(by='URL')  # backend quicksort

previous_url = ''
for i in stories_a.index:
    current_url = stories_a.ix[i, 'URL']
    if current_url == previous_url:
        stories_a.drop(i, inplace=True)
    previous_url = current_url

time_elapsed = time.time() - start_time

print('Time elapsed 5A - sort + traverse: ' + str(time_elapsed))

# Time elapsed 5A - sort + traverse: 15.055665969848633

# SECOND IMPLEMENTATION: hashing each row r to a number h(r) between 0 and N = 2^20-1

stories_b = pd.read_csv('data/stories_orig.csv')

hash_table = [[] for i in range(2 ** 20)]


def hash_function(date, url):
    '''start hash with publish date, then for each character add the ordinal value to the index. finally, find remainder
    of dividing by 2^20
    '''
    hashed_index = 0
    #if isinstance(date, str):
    #    hashed_index = int(date.replace('-', ''))  # remove - from date to a void ValueError
    for character in str(date)+url:
        hashed_index += ord(character)  # multiply by index
    return hashed_index % (2 ** 20)


start_time = time.time()

# store data in hash table
for index, row in stories_b.iterrows():
    date, url = row[['PUBLISHED', 'URL']]
    hashed_index = hash_function(date, url)
    hash_table[hashed_index].append(row.to_dict())  #

print("done hashing ", time.time() - start_time)

# deduplicate entries
for i, hashed_list in enumerate(hash_table):
    if len(hashed_list) > 1:  # potential dupes
        urls = []
        for j, entry in enumerate(hashed_list):
            url = entry['URL']
            if url in urls:
                del hash_table[i][j]
            else:
                urls.append(url)

time_elapsed = time.time() - start_time

print('Time elapsed 5B - hashing: ' + str(time_elapsed))
# 5B: 239.42458391189575
#Time elapsed 5B - hashing: 465.03688859939575