import sys
sys.path.append("../")

from sql_logic import Database_Instance
import matplotlib.pyplot as plt
import numpy as np
import vars

artist_file = vars.db_filenames[0]
artist_db = Database_Instance('../db_files/' + artist_file)

res = [a[1] for a in artist_db.query('''
    SELECT id, track_count FROM surface_artist_data where track_count < 200
''')]

plt.hist(res, bins=50)  # density=False would make counts
plt.ylabel('Number of Artists')
plt.xlabel('Track Count');
plt.show()
