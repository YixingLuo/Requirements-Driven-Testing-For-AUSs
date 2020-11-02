function [c,ceq] = myconuuv_normal(x)
c=[];
ceq=[];
global uuv
global pastdistance
global pasttime
global pastenergy
global pastaccuracy
global x_pre
global energy_control_pre
global dis_control_pre
global pole

%% time
time_left = uuv.time_target - pasttime;

%% control signal at previous adaptation step energy
engy_pre = 0;
for i = 1:uuv.N_s
    if uuv.s_work(i) == 1
        engy_pre = engy_pre + x_pre(i)*uuv.s_energy(i);
    end
end

%% energy_control
energy_control_now = energy_control_pre + pole*((uuv.energy_target-pastenergy)/(time_left) - engy_pre);

%% distance signal at previous adaptation step energy
dis_pre = 0;
for i = 1:uuv.N_s
    if uuv.s_work(i) == 1
        dis_pre = dis_pre + x_pre(i)*uuv.s_speed(i);
    end
end

%% distance_control
dis_control_now = dis_control_pre + pole*((uuv.distance_target-pastdistance)/(time_left) - dis_pre);


%% accuracy
acc = 0;
for i = 1:uuv.N_s
    if uuv.s_work(i) == 1
        acc = acc + x(i)*uuv.s_accuracy(i);
    end
end
accuracy  = (pastaccuracy * pasttime + acc * time_left) / (pasttime + time_left);




% c = [c, - accuracy + uuv.acc_budget];
% c = [c, - distance + uuv.distance_target];
% c = [c, energy - uuv.energy_target];
 


sum = 0;
for i = 1:uuv.N_s
    if uuv.s_work(i) == 1
        sum = sum + x(i);
    end
end
ceq = [ceq, sum-1];

engy = 0;
for i = 1:uuv.N_s
    if uuv.s_work(i) == 1
        engy = engy + x(i)*uuv.s_energy(i);
    end
end
ceq = [ceq, engy - energy_control_now];

speed = 0;
for i = 1:uuv.N_s
    if uuv.s_work(i) == 1
        speed = speed + x(i)*uuv.s_speed(i);
    end
end
ceq = [ceq, speed - dis_control_now];
