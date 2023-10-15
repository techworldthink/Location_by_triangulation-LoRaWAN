import numpy as np
from scipy.optimize import minimize
import datetime

# datetime to epoch time
def datetime_in_epoch(timestamp):
    dt = datetime.datetime.strptime(timestamp[:-4], '%Y-%m-%dT%H:%M:%S.%f')
    # Convert the datetime object to epoch microseconds
    epoch_microseconds = int(dt.timestamp() * 1000000)
    epoch_nanoseconds = str(epoch_microseconds) + str(timestamp[-4:-1])
    return epoch_nanoseconds


def tdoa_objective_function(x, tdoa, gateway_locations):
    # x[0], x[1] represent the device's x, y coordinates respectively
    device_position = np.array([x[0], x[1]])
    squared_distance = np.zeros(len(tdoa))
    # Calculate squared distance difference between device and each anchor
    for i in range(len(tdoa)):
        anchor_position = gateway_locations[i]
        # Euclidean distance formula
        distance = np.linalg.norm(device_position - anchor_position)
        tdoa_distance = tdoa[i] * SPEED_OF_LIGHT  # Speed of light
        squared_distance[i] = (distance - tdoa_distance) ** 2
    # Sum of squared distance differences
    return np.sum(squared_distance)

# find location
def tdoa_triangulate(tdoa, gateway_locations, initial_guess):
    result = minimize(tdoa_objective_function, initial_guess, args=(tdoa, gateway_locations), method='Nelder-Mead')
    device_location = result.x[:2]
    return device_location

# find time of arrival
def find_tdoa(datetime_list):
    acc_nano = 0.000000000001
    data = []
    for iter in range(0,len(datetime_list)-1):
        data.append((int(datetime_list[iter]) - int(datetime_list[iter+1]))*acc_nano)
    data.append((int(datetime_list[len(datetime_list)-1]) - int(datetime_list[0]))*acc_nano)
    return data

    
# Initial guess for device location
initial_guess = np.array([0.5, 0.5])
# Speed of light in meters per second
SPEED_OF_LIGHT = 299792458

# Perform triangulation
def triangulate(timestamps,locations):
    print("--Triangulate")
    # convert timestamp to epoch format
    timestamps_epoch = [datetime_in_epoch(each) for each in timestamps]
    # find time of arrival of each pair of gateways
    tdoa = find_tdoa(timestamps_epoch)
    # gateway locations
    gateway_locations = np.array(locations)
    # return location of the node
    return tdoa_triangulate(tdoa, gateway_locations, initial_guess)

