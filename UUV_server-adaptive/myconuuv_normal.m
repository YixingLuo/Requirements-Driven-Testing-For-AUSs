function [c,ceq] = myconuuv_normal(x)
c=[];
ceq=[];
global uuv
global pastdistance
global pasttime
global pastenergy
global pastaccuracy

%% time
time_left = uuv.time_target - pasttime;

%% accuracy
acc = 0;
for i = 1:uuv.N_s
    if uuv.s_work(i) == 1
        acc = acc + x(i)*uuv.s_accuracy(i);
    end
end
accuracy  = (pastaccuracy * pasttime + acc * time_left) / (pasttime + time_left);

%% distance
speed = 0;
for i = 1:uuv.N_s
    if uuv.s_work(i) == 1
        speed = speed + x(i)*uuv.s_speed(i);
    end
end
distance = pastdistance + time_left * speed;

%% energy
engy = 0;
for i = 1:uuv.N_s
    if uuv.s_work(i) == 1
        engy = engy + x(i)*uuv.s_energy(i);
    end
end
energy = pastenergy + time_left * engy;

c = [c, - accuracy + uuv.acc_budget];
c = [c, - distance + uuv.distance_target];
c = [c, energy - uuv.energy_target];
 


sum = 0;
for i = 1:uuv.N_s
    if uuv.s_work(i) == 1
        sum = sum + x(i);
    end
end
ceq = [ceq, sum-1];
% c = [c, sum-1];

