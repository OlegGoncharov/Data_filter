from pykalman import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.io as sio


X = sio.loadmat('X.mat')
Y = sio.loadmat('Y.mat')
Z = sio.loadmat('Z.mat')

X = X['X']
X = X[1:]
Y = Y['Y']
Y = Y[1:]
Z = Z['Z']
Z = Z[1:]

measurements = np.column_stack((X,Y))

initial_state_mean = [measurements[0, 0],
                      0,
                      measurements[0, 1],
                      0]

transition_matrix = [[1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 1]]

observation_matrix = [[1, 0, 0, 0],
                      [0, 0, 1, 0]]

kf1 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean)

kf1 = kf1.em(measurements, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)




time_before = time.time()
n_real_time = 3

kf3 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean,
                  observation_covariance = 50*kf1.observation_covariance,
                  em_vars=['transition_covariance', 'initial_state_covariance'])

kf3 = kf3.em(measurements[:-n_real_time, :], n_iter=5)
(filtered_state_means, filtered_state_covariances) = kf3.filter(measurements[:-n_real_time,:])

print("Time to build and train kf3: %s seconds" % (time.time() - time_before))

x_now = filtered_state_means[-1, :]
P_now = filtered_state_covariances[-1, :]
x_new = np.zeros((n_real_time, filtered_state_means.shape[1]))
i = 0

for measurement in measurements[-n_real_time:, :]:
    time_before = time.time()
    (x_now, P_now) = kf3.filter_update(filtered_state_mean = x_now,
                                       filtered_state_covariance = P_now,
                                       observation = measurement)
    print("Time to update kf3: %s seconds" % (time.time() - time_before))
    x_new[i, :] = x_now
    i = i + 1

plt.figure(1)
old_times = range(measurements.shape[0] - n_real_time)
new_times = range(measurements.shape[0]-n_real_time, measurements.shape[0])
times = range(measurements.shape[0])
plt.plot(times, measurements[:, 0], 'bo',
         times, measurements[:, 1], 'ro',
         old_times, filtered_state_means[:, 0], 'b--',
         old_times, filtered_state_means[:, 2], 'r--',
         new_times, x_new[:, 0], 'b-',
         new_times, x_new[:, 2], 'r-')
##plt.legend((line1, line2, line3, line4, line5, line6), ('measurements0', 'measurements1', 'filtered_state_means1','filtered_state_means2','new1kf3','new2kf3'))
sio.savemat('Ant1_two_antennas_XY_real_time.mat', {'X_filtered':filtered_state_means[:, 0],'Y_filtered': filtered_state_means[:, 2]})

plt.show()
