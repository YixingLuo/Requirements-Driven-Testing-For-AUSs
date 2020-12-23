% 1: uuv = EnergyBudget(uuv, 5 * 1e6);
% 2: uuv = DistanceBudget(uuv, 105*1000);
% 3: uuv = AccuracyBudget(uuv, 0.85);
% 4: uuv = SensorError(uuv, 3, 0.43);
% 5: uuv = SensorFailure(uuv, 4);
% 6: uuv = EnergyDisturbance(uuv, 1, 190);
function [condition, index] = randomsituation(num,k)
% disturb = randperm(7);
global uuv
global datafolder
uuv = UnmannedUnderwaterVehicle();
% l = 1:1:15;
% disturb = randi([1,6],1,l(k));
disturb = unidrnd(4,1,k);
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
        acc_ratio = 40*rand;
%             acc = uuv.s_accuracy(idx)*acc_ratio/100;
        condition(i,:) = [1,idx,acc_ratio];
    elseif disturb(i) == 2
        idx = unidrnd(5);
        energy_ratio = 40*rand;
%             energy = uuv.s_energy(idx)*energy_ratio/100;
        condition(i,:) = [2,idx,energy_ratio];
   elseif disturb(i) == 3
        idx = unidrnd(5);
        speed_ratio = 40*rand;
%             speed = uuv.s_speed(idx)*speed_ratio/100;
        condition(i,:) = [3,idx,speed_ratio];   
    elseif disturb(i) == 4
        idx = unidrnd(5);
        if any (idx == failure_list)
            idx = unidrnd(5);
        end
        condition(i,:) = [4,idx,0];
    elseif disturb(i) == 5 
        idx = unidrnd(5);
        energy_target_ratio = 20*rand;
        condition(i,:) = [5,0,energy_target_ratio]; 
    elseif disturb(i) == 6
        idx = unidrnd(5);
        dis_target_ratio = 20*rand;
        condition(i,:) = [6,0,dis_target_ratio]; 
    end
end
name = datafolder + '/condition' + string(num) + '.mat';
save(name, 'condition');
name = datafolder + '/index' + string(num) + '.mat';
save(name, 'index');



