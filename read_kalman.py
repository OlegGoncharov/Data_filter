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

measurements = np.column_stack((X,Y,Z))

initial_state_mean = [measurements[0, 0],
                      0,
                      measurements[0, 1],
                      0,
                      measurements[0, 2],
                      0]

transition_matrix = [[1, 0.0178, 0, 0, 0, 0],
                     [0, 0.0178, 0, 0, 0, 0],
                     [0, 0, 1, 0.0178, 0, 0],
                     [0, 0, 0, 0.0178, 0, 0],
                     [0, 0, 0, 0, 1, 0.0178],
                     [0, 0, 0, 0, 0, 0.0178]]

observation_matrix = [[1, 0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0]]

kf1 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean)

kf1 = kf1.em(measurements, n_iter=10)
(smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)

time_before = time.time()
n_real_time = 3

kf3 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean,
                  observation_covariance = 120*kf1.observation_covariance,
                  em_vars=['transition_covariance', 'initial_state_covariance'])

kf3 = kf3.em(measurements[:-n_real_time, :], n_iter=10)
(filtered_state_means, filtered_state_covariances) = kf3.filter(measurements[:-n_real_time,:])

x_now = filtered_state_means[-1, :]
P_now = filtered_state_covariances[-1, :]
x_new = np.zeros((n_real_time, filtered_state_means.shape[1]))
i = 0

for measurement in measurements[-n_real_time:, :]:
    time_before = time.time()
    (x_now, P_now) = kf3.filter_update(filtered_state_mean = x_now,
                                       filtered_state_covariance = P_now,
                                       observation = measurement)
    x_new[i, :] = x_now
    i = i + 1
sio.savemat('Ant1_two_antennas_XYZ_real_time.mat', {'X_filtered':filtered_state_means[:, 0],'Y_filtered': filtered_state_means[:, 2],'Z_filtered':filtered_state_means[:, 4]})

print("Дисперсия до фильтрации X = " + str(np.var(measurements[:, 0])))
print("Дисперсия после фильтрации X = " + str(np.var(filtered_state_means[:, 0])))

print("Дисперсия до фильтрации Y = " + str(np.var(measurements[:, 1])))
print("Дисперсия после фильтрации Y = " + str(np.var(filtered_state_means[:, 2])))

print("Дисперсия до фильтрации Z = " + str(np.var(measurements[:, 2])))
print("Дисперсия после фильтрации Z = " + str(np.var(filtered_state_means[:, 4])))


plt.show()
