clc
clear
data1 = [];
usage_plan1 = [];
count = [];
iternum = 500;
planning_time1 = zeros(360,iternum);
planning_time2 = zeros(360,iternum);
planning_time3 = zeros(360,iternum);
rate_list3 = zeros(100,100);
tag_list3 = zeros(100,100);
num = 0;


tstart =tic; 
while(1)
    tused = toc(tstart) ;
    if tused > 3*3600 || num == 10000
        time = datestr(now,30);
        path = strcat(datafolder,'/data',time);
        save(path);
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
    
    if  ((data_(1) > data(1)) &&  data_(3)>=data(3) && data_(5)>= data(5) ) ||((data_(3) > data(3)) &&  data_(5)>=data(5) && data_(1)>= data(1)) || ((data_(5) > data(5)) &&  data_(1)>=data(1) && data_(3)>= data(3))
        count = [count,num];
    end
    
    
end




