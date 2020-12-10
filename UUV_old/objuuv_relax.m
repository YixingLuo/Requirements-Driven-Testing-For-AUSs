function f = objuuv_relax(x)
sum = 0;
global uuv
global pastdistance
global pasttime
global pastenergy
global pastaccuracy

f=[];

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

f = ((accuracy - uuv.acc_target)/(uuv.acc_target-uuv.acc_budget)).^2 + ((distance - uuv.distance_target) / (uuv.distance_target-uuv.distance_budget)).^2 + ((uuv.energy_target - energy) / (uuv.energy_budget - uuv.energy_target)).^2;
% f = max(0,(uuv.acc_target-accuracy)/(uuv.acc_target-uuv.acc_budget)) + max(0,(uuv.distance_target-distance)/ (uuv.distance_target-uuv.distance_budget)) + max(0,(energy -  uuv.energy_target)/ (uuv.energy_budget - uuv.energy_target));
