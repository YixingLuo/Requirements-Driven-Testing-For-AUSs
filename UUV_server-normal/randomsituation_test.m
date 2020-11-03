function Population = randomsituation_test
x=[];
global num_incidents
global uuv
uuv = UnmannedUnderwaterVehicle();
l = 1:1:15;
disturb = randi([1,4],1,l(num_incidents));
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
            acc_ratio = 20*rand;
%             acc = uuv.s_accuracy(idx)*acc_ratio/100;
            condition(i,:) = [1,idx,acc_ratio];
        elseif disturb(i) == 2
            idx = unidrnd(5);
            energy_ratio = 20*rand;
%             energy = uuv.s_energy(idx)*energy_ratio/100;
            condition(i,:) = [2,idx,energy_ratio];
       elseif disturb(i) == 3
            idx = unidrnd(5);
            speed_ratio = 20*rand;
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
    for i = 1: length(disturb)
%         x0(i,1) = index (i);
%         x0(i,2) = condition(i,1);
%         x0(i,3) = condition(i,2);
%         x0(i,4) = condition(i,3);
        x((i-1)*4+1) = index (i);
        x((i-1)*4+2) = condition(i,1);
        x((i-1)*4+3) = condition(i,2);
        x((i-1)*4+4) = condition(i,3);
    end
end
