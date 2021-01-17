import sys
sys.path.append("../")

from sql_logic import Database_Instance
import pickle
import vars

dbs = [Database_Instance('../db_files/' + f) for f in vars.db_filenames]
id_sets = []

all_set = set()

for i in range(len(dbs)):
    curr_set = set()
    for a in dbs[i].query('''SELECT id FROM surface_artist_data'''):
        curr_set.add(a[0])
        all_set.add(a[0])
    id_sets.append(curr_set)

common_ids = set.intersection(*id_sets)

profile_data = {}

for i in range(len(dbs)):
    res = dbs[i].query('''SELECT id, followers_count, track_count, verified FROM surface_artist_data''')
    for id, followers, track, verified in res:
        if id in common_ids:
            if id in profile_data:
                profile_data[id]['followers_count'].append(followers)
                profile_data[id]['track_count'].append(track)
                profile_data[id]['verified'].append(track)
            else:
                profile_data[id] = {}
                profile_data[id]['followers_count'] = [followers]
                profile_data[id]['track_count'] = [track]
                profile_data[id]['verified'] = [verified]

ids_to_remove = set()

for id in common_ids:
    if(profile_data[id]['followers_count'][len(dbs) - 1] < 1000 or profile_data[id]['verified'][len(dbs) - 1] == 1):
        ids_to_remove.add(id)

common_ids = common_ids.difference(ids_to_remove)

to_dump = {}
to_dump['common_ids'] = common_ids
to_dump['profile_data'] = profile_data

pickle.dump(to_dump, open('data.pickle', 'wb'))
