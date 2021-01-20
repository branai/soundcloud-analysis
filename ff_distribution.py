from sql_logic import Database_Instance
import matplotlib.pyplot as plt
import vars

# Following Count Distribution for Artist Followers 
def show_following_distribution(filename, ids_to_plot):
    user_file = filename
    artist_db = Database_Instance(user_file)

    for curr in ids_to_plot.keys():
        try:
            res = [a[1] for a in artist_db.query('''
                SELECT id, followings_count FROM follower_data_{} where followings_count < 500
            '''.format(curr))]

            plt.hist(res, bins=50)
            plt.title('Following Count Distribution for the Followers of Artist {}'.format(str(ids_to_plot[curr])))
            plt.ylabel('Frequency')
            plt.xlabel('Following Count')
            #plt.show()
            plt.savefig('images/Artist{}.png'.format(str(ids_to_plot[curr])))
            plt.clf()
        except:
            print("ID " + str(ids_to_plot) + " given possibly not in DB")



show_following_distribution('db_files/followers_pot.db', vars.check_pot_ids)
show_following_distribution('db_files/followers_bad.db', vars.check_bad_ids)
#show_following_distribution('db_files/followers_good.db', vars.check_good_ids)
