clc
clear
data1 = [];
usage_plan1 = [];
iternum = 100;
planning_time1 = zeros(360,iternum);
planning_time2 = zeros(360,iternum);
planning_time3 = zeros(360,iternum);
rate_list3 = zeros(100,100);
tag_list3 = zeros(100,100);



for num = 1:15*iternum
    fprintf('current iteration %d\n', num);
    k = ceil(num/iternum);

    [condition, indextemp] = randomsituation(num,k);
    index(num,:) = indextemp;

    iter = mod(num,iternum);
    if iter == 0
        iter = iternum;
    end
    data = zeros(1,6);
    [data,usage_plan,planning_time] = uuv_normal(num, indextemp);
    while data(1)>=0.95 && data(3) == 1 && data(5)==1
        [data,usage_plan,planning_time] = uuv_normal(num, indextemp);
    end
    data1(num,:) = data;
    usage_plan1 = [usage_plan1 ; usage_plan];
    planning_time =[planning_time; zeros(360-length(planning_time),1)] ;              
    planning_time1(:,iter) = planning_time;

    if mod(num,iternum)==0
        index = [];
    end
end
time = datestr(now,30);
name = 'data' + string(time) + '.mat';
save(name);




