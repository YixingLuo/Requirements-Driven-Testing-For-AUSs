clc
clear
data1 = [];
usage_plan1 = [];
count = [];
num = 0;

datafolder = 'conditions3';
mkdir(datafolder);
addpath(datafolder);

tstart =tic; 
for num = 0:1:20000
    if num == 20000
        time = datestr(now,30);
        name = 'data' + string(time) + '.mat';
        save(name);
        break;
    end
    num = num + 1;
    fprintf('current iteration %d\n', num);
    k = 5;
    

    [condition, indextemp] = randomsituation(num,k);
    
    
    
    data = zeros(1,6);
    [data,usage_plan,planning_time] = uuv_normal(indextemp, condition);
    data1(num,:) = data;
    index(num,:) = indextemp;
    
    cond=[];
    for i = 1:length(indextemp)
        cond(i,1) = indextemp(i);
        cond(i,2) = condition(i,1);
        cond(i,3) = condition(i,2);
        cond(i,4) = condition(i,3);
    end
    name = 'condition' + string(num) + '.mat';
    path = strcat(datafolder,'/',name);
    save(path, 'cond');
    
end




