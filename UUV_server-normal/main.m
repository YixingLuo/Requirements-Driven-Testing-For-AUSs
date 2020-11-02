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

tstart =tic; 
while(1)
    tused = toc(tstart) ;
    if tused > 10*3600
        break;
    end
    num = num + 1;
    fprintf('current iteration %d\n', num);
    k = 5;
    

    [condition, indextemp] = randomsituation(num,k);
    index(num,:) = indextemp;
    forward = 36*ones(1,5);
    cc = 0;
    for i = 1:length(forward)
        if indextemp(i)-forward(i) < 6
            cc = cc + 1;
        end
    end
    indextemp2 = indextemp - 36;
    for i = 1:cc
        indextemp2(i) = i;
    end
    index2(num,:) = indextemp2;

    iter = mod(num,iternum);
    if iter == 0
        iter = iternum;
        
    end
    data = zeros(1,6);
    [data,usage_plan,planning_time] = uuv_normal(num, indextemp, condition);
    [data_,usage_plan,planning_time] = uuv_normal(num, indextemp2, condition);
    if (data_(1) > data(1)) && (abs(data_(3)-data(3)) < 1e-6) && (abs(data_(5)-data(5)) < 1e-6)
        count = [count,num];
        name = 'condition' + string(num) + '.mat';
        save(name, 'condition');
        name = 'index' + string(num) + '.mat';
        save(name, 'indextemp');
        data1(num,:) = data;
        data2(num,:) = data_;
    elseif (data_(3) > data(3)) && (abs(data_(1)-data(1)) < 1e-6) && (abs(data_(5)-data(5)) < 1e-6)
        count = [count,num];
        name = 'condition' + string(num) + '.mat';
        save(name, 'condition');
        name = 'index' + string(num) + '.mat';
        save(name, 'indextemp');
        data1(num,:) = data;
        data2(num,:) = data_;
    elseif (data_(5) > data(5)) && (abs(data_(1)-data(1)) < 1e-6) && (abs(data_(3)-data(3)) < 1e-6)
        count = [count,num];
        name = 'condition' + string(num) + '.mat';
        save(name, 'condition');
        name = 'index' + string(num) + '.mat';
        save(name, 'indextemp');
        data1(num,:) = data;
        data2(num,:) = data_;
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
time = datestr(now,30);
name = 'data' + string(time) + '.mat';
save(name);




