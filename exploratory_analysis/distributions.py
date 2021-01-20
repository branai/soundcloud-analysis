import sys
sys.path.append("../")

from sql_logic import Database_Instance
import matplotlib.pyplot as plt
import numpy as np
import vars
import utils


artist_file = vars.db_filenames[0]
artist_db = Database_Instance('../db_files/' + artist_file)

# Follower Count Distribution
res = [a[1] for a in artist_db.query('''
    SELECT id, followers_count FROM surface_artist_data where followers_count < 10000
''')]

plt.hist(res, bins=50)
plt.title('Follower Count Distribution')
plt.ylabel('Number of Artists')
plt.xlabel('Followers Count')
plt.show()


# Track Count Distribution
res = [a[1] for a in artist_db.query('''
    SELECT id, track_count FROM surface_artist_data where track_count < 200
''')]

plt.hist(res, bins=50)
plt.title('Track Count Distribution')
plt.ylabel('Number of Artists')
plt.xlabel('Track Count')
plt.show()

# Comments Count Distribution
res = [a[1] for a in artist_db.query('''
    SELECT id, comments_count FROM surface_artist_data where comments_count < 500
''')]

plt.hist(res, bins=50)
plt.title('Comments Count Distribution')
plt.ylabel('Number of Artists')
plt.xlabel('Comments Count')
plt.show()


# Likes Distribution
res = [a[1] for a in artist_db.query('''
    SELECT id, likes_count FROM surface_artist_data where likes_count < 2500
''')]

plt.hist(res, bins=50)
plt.title('Likes Count Distribution')
plt.ylabel('Number of Artists')
plt.xlabel('Likes Count')
plt.show()


# Maximum Percent Gain Distribution
id_to_followers = {}

for f in vars.db_filenames:
    db = Database_Instance('../db_files/' + f)
    for a in db.query('''SELECT id, followers_count FROM surface_artist_data'''):
        if a[0] in id_to_followers:
            id_to_followers[a[0]].append(a[1])
        else:
            id_to_followers[a[0]] = [a[1]]

max_followers = []
max_percent_gain = []
max_followers_bad = []
max_percent_gain_bad = []
ids = []
ids_bad = []

for id in id_to_followers.keys():
    try:
        max(id_to_followers[id])
        max(utils.percent_change(id_to_followers[id]))
        max_followers_bad.append(max(id_to_followers[id]))
        max_percent_gain_bad.append(max(utils.percent_change(id_to_followers[id])))
    except:
        print(id_to_followers[id])

plt.plot(max_followers, max_percent_gain, 'b.')

plt.ylabel('Max Percent Gain')
plt.xlabel('Max Followers')

plt.show()
