clc
clear
result = [];
count = zeros(1,8);
count_list = [];
for iter = 0:1:199
    filename = 'Datalog-2020-12-12-0-23/interval-results-' + string(iter);
    
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
    if mod(iter+1,1) == 0
%         mod(iter+1,50), iter
        count_list = [count_list; count];
    end  
    
end
count_list