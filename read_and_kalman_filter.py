from pykalman import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio


X = sio.loadmat('X.mat')
Y = sio.loadmat('Y.mat')
Z = sio.loadmat('Z.mat')

X = X['X']
X = X[1:]
print("X = "+ str(X))
Y = Y['Y']
Y = Y[1:]
print("Y = "+ str(Y))
Z = Z['Z']
Z = Z[1:]
print("Z = "+ str(Z))



measurements = np.column_stack((X,Y,Z))

initial_state_mean = [measurements[0, 0],
                      0,
                      measurements[0, 1],
                      0,
                      measurements[0, 2],
                      0]
transition_matrix = [[1,0.0178,0,0,0,0],
                     [0,0.0178,0,0,0,0],
                     [0,0,1,0.0178,0,0],
                     [0,0,0,0.0178,0,0],
                     [0,0,0,0,1,0.0178],
                     [0,0,0,0,0,0.0178]]


observation_matrix = [[1,0,0,0,0,0],
                      [0,0,1,0,0,0],
                      [0,0,0,0,1,0]]

kf1 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean)

kf1 = kf1.em(measurements, n_iter=10)


kf2 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean,
                  observation_covariance = 100*kf1.observation_covariance,
                  em_vars=['transition_covariance', 'initial_state_covariance'])

kf2 = kf2.em(measurements, n_iter=10)
(smoothed_state_means, smoothed_state_covariances)  = kf2.smooth(measurements)











print("Дисперсия до фильтрации X = " + str(np.var(measurements[:, 0])))
print("Дисперсия после фильтрации X = " + str(np.var(smoothed_state_means[:, 0])))

print("Дисперсия до фильтрации Y = " + str(np.var(measurements[:, 1])))
print("Дисперсия после фильтрации Y = " + str(np.var(smoothed_state_means[:, 1])))

print("Дисперсия до фильтрации Z = " + str(np.var(measurements[:, 2])))
print("Дисперсия после фильтрации Z = " + str(np.var(smoothed_state_means[:, 2])))

sio.savemat('Ant1_two_antennas.mat', {'X_filtered':smoothed_state_means[:, 0], 'Y_filtered':smoothed_state_means[:, 1], 'Z_filtered':smoothed_state_means[:, 2]})
