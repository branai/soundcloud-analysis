from sql_logic import Database_Instance
import matplotlib.pyplot as plt
import vars
import numpy as np

from scipy.spatial.distance import jensenshannon
import math
normal = []

# Following Count Distribution for Artist Followers
def show_following_distribution(filename, ids_to_plot):
    user_file = filename
    artist_db = Database_Instance(user_file)

    distributions = []

    for curr in ids_to_plot.keys():
        try:
            res = [a[1] for a in artist_db.query('''
                SELECT id, followings_count FROM follower_data_{} where followings_count < 500
            '''.format(curr))]

            n, bins, patches = plt.hist(res, bins=50)

            if len(normal) != 0:
                plt.title('Following Count Distribution for the Followers of Artist {}'.format(str(ids_to_plot[curr])))
                plt.ylabel('Frequency')
                plt.xlabel('Following Count')
                plt.savefig('./images/BadArtist{}.png'.format(str(ids_to_plot[curr])))

                # Calculate Jensen-Hannon Divergence
                jh = math.sqrt(jensenshannon(normal[0], n))
                plt.annotate("JH: " + str(jh)[:8], xy=(0.7, 0.9), xycoords='axes fraction', fontsize=14, color='purple')
                plt.savefig('./images/JH_GoodArtist{}.png'.format(str(ids_to_plot[curr])))
                #plt.show()

            plt.clf()
            distributions.append(n)
        except:
            print("ID " + str(ids_to_plot) + " given possibly not in DB")
    return bins, distributions


x, normal = show_following_distribution('db_files/followers_good.db', vars.check_good_ids)

show_following_distribution('db_files/followers_good.db', vars.check_good_ids)
show_following_distribution('db_files/followers_bad.db', vars.check_bad_ids)
show_following_distribution('db_files/followers_pot.db', vars.check_pot_ids)
show_following_distribution('db_files/followers_pot.db', vars.check_bad_ids)
