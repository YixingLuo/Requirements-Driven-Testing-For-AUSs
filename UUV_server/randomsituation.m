% 1: uuv = EnergyBudget(uuv, 5 * 1e6);
% 2: uuv = DistanceBudget(uuv, 105*1000);
% 3: uuv = AccuracyBudget(uuv, 0.85);
% 4: uuv = SensorError(uuv, 3, 0.43);
% 5: uuv = SensorFailure(uuv, 4);
% 6: uuv = EnergyDisturbance(uuv, 1, 190);
function [condition, index] = randomsituation(num,k)
% disturb = randperm(7);
global uuv
uuv = UnmannedUnderwaterVehicle();
l = 1:1:15;
disturb = randi([1,3],1,l(k));
a=2:359;
K=randperm(length(a));
N=length(disturb);
index1 = a(K(1:N));
% index1 = randperm(359,length(disturb));
index = sort(index1);
condition = [];
failure_list = [];
for i = 1: length(disturb)
    if disturb(i) == 1
        idx = unidrnd(5);   
        acc_ratio = unidrnd(100);
        acc = uuv.s_accuracy(idx)*acc_ratio/100;
        condition(i,:) = [1,idx,acc];
    elseif disturb(i) == 2
        idx = unidrnd(5);
        energy_ratio = 100 + unidrnd(100);
        energy = uuv.s_energy(idx)*energy_ratio/100;
        condition(i,:) = [2,idx,energy];
   elseif disturb(i) == 3
        idx = unidrnd(5);
        speed_ratio = unidrnd(100);
        speed = uuv.s_speed(idx)*speed_ratio/100;
        condition(i,:) = [3,idx,speed];   
    elseif disturb(i) == 4
        idx = unidrnd(5);
        if any (idx == failure_list)
            idx = unidrnd(5);
        end
        condition(i,:) = [4,idx,-1];
    end
end
name = 'condition' + string(num) + '.mat';
save(name, 'condition');
name = 'index' + string(num) + '.mat';
save(name, 'index');



