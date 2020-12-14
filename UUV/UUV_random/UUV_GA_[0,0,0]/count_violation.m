clc
clear
result = [];
count = zeros(1,8);
count_list = [];
for iter = 0:1:1000
    filename = 'Datalog-2020-12-14-10-40/interval-results-' + string(iter) + '.mat';
    if exist(filename,'file')==0
        count_list = [count_list; count];
        break
    end
    
    data = load(filename);
    data1 = data.scores;
    
    [m,n] = size(data1);
    
    for i = 1:1:m
        temp_result = data1(m,:);
        flag = zeros(1,3);
        if abs(temp_result(1))< 0.9
            flag(1) = 1;
        end
        if abs(temp_result(2))< 100*1000
            flag(2) = 1;
        end
        if abs(temp_result(3))> 5.4*1e6
            flag(3) = 1;
        end
        result = [result; flag];
        sum = flag(1)*2^0 + flag(2)*2^1 + flag(3)*2^2 + 1;
        count(sum) = count(sum) + 1;
        
    end
    if mod(iter+1,50) == 0
%         mod(iter+1,50), iter
        count_list = [count_list; count];
    end  
    
end
count_list, size(result,1)