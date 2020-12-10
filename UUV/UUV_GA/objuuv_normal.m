function f = objuuv_normal(x)
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



% f = - accuracy;
f = -acc;
