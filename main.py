import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
import math
import pickle
import vars
import utils


loaded = pickle.load(open('data.pickle', 'rb'))

common_ids = loaded['common_ids']
profile_data = loaded['profile_data']

#Id to root mean square dict
id_to_rmse = {}

#Id to slope dict
id_to_slope = {}

#Id to max track difference before greatest percent gain in followerts
id_to_track = {}

for id in common_ids:
    # Get percent change set for followers
    #TODO: Should percent change be from minimum follower count???
    points = utils.percent_change(profile_data[id]['followers_count'])
    x = np.array([1,2,3,4,5])

    # Find regression line for percent change set
    regline = linregress(x, points)

    if regline.slope >= 0:
        # Calculate rmse
        rmse = 0
        for i in range(len(points)):
            if(regline.slope > 0):
                predicted = (regline.slope * x[i]) + regline.intercept
                rmse += (predicted - points[i])**2

        rmse = rmse / len(points)
        rmse = math.sqrt(rmse)

        # calculate max track difference before greatest percent gain in followerts
        track_count = profile_data[id]['track_count']
        max_percent_change_index = points.index(max(points))
        id_to_track[id] = min(track_count[max_percent_change_index], track_count[max_percent_change_index + 1]) - track_count[0]
        id_to_rmse[id] = rmse
        id_to_slope[id] = regline.slope

# (slope * error): id dict
combined_to_id = {(v * id_to_slope[k]): k for k, v in sorted(id_to_rmse.items(), key=lambda item: item[1], reverse=True)}
sorted_combined = list(combined_to_id.keys())


blue_x = []
blue_y = []
red_x = []
red_y = []

# Plot top 500 combined error and slope
for i in range(500):
    com = sorted_combined[i]
    curr = combined_to_id[com]
    error = id_to_rmse[curr]
    trajectory = id_to_slope[curr]

    #TODO: incorporate mtdbgpg into y value???
    if curr not in vars.potential_flag:
        blue_x.append(error)
        blue_y.append(trajectory)
    else:
        red_x.append(error)
        red_y.append(trajectory)
    #plt.annotate(str(curr), (error, trajectory))

plt.plot(blue_x, blue_y, 'b.', label='Unverified Follower Distribution')
plt.plot(red_x, red_y, 'r.', label='Verified Irregular Follower Distribution')

plt.title("Trajectory to Error Plot for Artists")
plt.ylabel("Regression Line Trajectory")
plt.xlabel('Error in Regression Line')
plt.legend()
plt.show()
