import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
import math
import pickle
import vars

loaded = pickle.load(open('data.pickle', 'rb'))

common_ids = loaded['common_ids']
profile_data = loaded['profile_data']

def percent_change(s):
    p_change = []
    for i in range(1, len(s)):
        p_change.append((s[i] - s[i - 1])/s[i - 1])
    return p_change

id_to_rmse = {}
id_to_slope = {}

for id in common_ids:
    points = percent_change(profile_data[id]['followers_count'])
    x = np.array([1,2,3,4,5])
    regline = linregress(x, points)

    rmse = 0
    for i in range(len(points)):
        if(regline.slope > 0):
            predicted = (regline.slope * x[i]) + regline.intercept
            rmse += (predicted - points[i])**2

    rmse = rmse / len(points)
    rmse = math.sqrt(rmse)

    id_to_rmse[id] = rmse
    id_to_slope[id] = regline.slope

rmse_to_id = {v: k for k, v in sorted(id_to_rmse.items(), key=lambda item: item[1], reverse=True)}
sorted_rmse = list(rmse_to_id.keys())


for i in range(500):
    error = sorted_rmse[i]
    curr = rmse_to_id[error]
    trajectory = id_to_slope[curr]

    if curr not in vars.potential_flag:
        plt.plot(error, trajectory, 'b.')
        plt.annotate(str(curr), (error, trajectory))
    else:
        plt.plot(error, trajectory, 'r.')
        plt.annotate(str(curr), (error, trajectory))

plt.ylabel("Prediction Trajectory")
plt.xlabel('Error in Prediction')
plt.show()
