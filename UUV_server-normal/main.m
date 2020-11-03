clc
clear
data1 = [];
data2 = [];
usage_plan1 = [];
count = [];
iternum = 500;
planning_time1 = zeros(360,iternum);
planning_time2 = zeros(360,iternum);
planning_time3 = zeros(360,iternum);
rate_list3 = zeros(100,100);
tag_list3 = zeros(100,100);
num = 0;

datafolder = 'soft-goal-violation-2';
mkdir(datafolder);
addpath(datafolder);

tstart =tic; 
while(1)
    tused = toc(tstart) ;
    if tused > 3*3600 || num == 1000
        time = datestr(now,30);
        path = strcat(datafolder,'/data',time);
        save(path);
        break;
    end
    num = num + 1;
    fprintf('current iteration %d\n', num);
    k = 5;
    

    [condition, indextemp] = randomsituation(num,k);
    
    %% move the incidents forward 36 time step
%     forward = 36*ones(1,5);
%     cc = 0;
%     for i = 1:length(forward)
%         if indextemp(i)-forward(i) < 6
%             cc = cc + 1;
%         end
%     end
%     indextemp2 = indextemp - 36;
%     for i = 1:cc
%         indextemp2(i) = i;
%     end
   
    %% increase the magnitude
    indextemp2 = indextemp;
    condition2 = condition;
    for i = 1:size(condition,1)
        condition2(i,3) = condition(i,3)*1.05;
    end
    
    
    data = zeros(1,6);
    [data,usage_plan,planning_time] = uuv_normal(indextemp, condition);
    [data_,usage_plan,planning_time] = uuv_normal(indextemp2, condition2);
    data1(num,:) = data;
    data2(num,:) = data_;
    index(num,:) = indextemp;
    index2(num,:) = indextemp2;
    
    cond=[];
    for i = 1:length(indextemp)
        cond(i,1) = indextemp(i);
        cond(i,2) = condition(i,1);
        cond(i,3) = condition(i,2);
        cond(i,4) = condition(i,3);
    end
    name = 'condition' + string(num) + '.mat';
    path = strcat(datafolder,'/',name);
    save(path, 'condition');
    
    if  ((data_(1) > data(1)) &&  data_(3)>=data(3) && data_(5)>= data(5) ) ||((data_(3) > data(3)) &&  data_(5)>=data(5) && data_(1)>= data(1)) || ((data_(5) > data(5)) &&  data_(1)>=data(1) && data_(3)>= data(3))
        count = [count,num];
%         name = 'index' + string(num) + '.mat';
%         path = strcat(datafolder,'/',name);
%         save(path, 'indextemp');
    end
%     while data(1)>=0.95 && data(3) == 1 && data(5)==1
%         [data,usage_plan,planning_time] = uuv_normal(num, indextemp);
%     end
%     data1(num,:) = data;
%     data2(num,:) = data_;
%     usage_plan1 = [usage_plan1 ; usage_plan];
%     planning_time =[planning_time; zeros(360-length(planning_time),1)] ;              
%     planning_time1(:,iter) = planning_time;

%     if mod(num,iternum)==0
%         index = [];
%     end
end




