close all; clc;
clear;
load('matlab.mat')
load('Ant1_two_antennas_XYZ_real_time.mat')
figure(1)
hold on
time = RoKiX.time;
X = RoKiX.x';
Y = RoKiX.y';
Z = RoKiX.z';
t_stop = length(X)-4;
plot(time(1:t_stop),X(1:t_stop));
plot(time(1:t_stop),Y(1:t_stop));
plot(time(1:t_stop),Z(1:t_stop));

time = time(1:end-1)';
plot(time(1:t_stop),X_filtered(1:t_stop),'LineWidth',2);
plot(time(1:t_stop),Y_filtered(1:t_stop),'LineWidth',2);
plot(time(1:t_stop),Z_filtered(1:t_stop),'LineWidth',2);
xlim([time(1) time(t_stop)])
grid on
xlabel('t, c')
legend('X','Y','Z','X фильтрованное','Y фильтрованное','Z фильтрованное')
ylabel('Координата, м')