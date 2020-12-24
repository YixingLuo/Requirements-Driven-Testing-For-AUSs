% clc
% clear
result = [];
count = zeros(1,8);
priority_list = [1,1,1; 
                 0,1,1;
                 1,0,1;
                 1,1,0;
                 0,0,1;
                 0,1,0;
                 1,0,0;
                 0,0,0;];
for iter = 1:1:1000
    
    
    filename = 'Datalog-2020-12-22-21-5/interval-results-' + string(iter) + '.mat';
    if exist(filename,'file')==0
%         count_list = [count_list; count_list];
        break
    end
    
    data = load(filename);
    data1 = data.fitness;
    
    [m,n] = size(data1);
    
    for i = 1:1:m
        temp_result = data1(i,:);
        flag = zeros(1,3);
        if abs(temp_result(1))< 0.9*0.9
            flag(1) = 1;
        end
        if abs(temp_result(2))< 100*0.95*1000
            flag(2) = 1;
        end
        if abs(temp_result(3))> 5.4*1.001*1e6
            flag(3) = 1;
        end
        result = [result; flag];
%         violation_pattern = flag(1)*2^0 + flag(2)*2^1 + flag(3)*2^2 + 1;
%         if violation_pattern > 0
%             count_list(violation_pattern) = count_list(violation_pattern) + 1;
%         end
        for j = 1:size(priority_list,1)
            if priority_list(j,:) == flag
                count(j) = count(j) + 1;
                break
            end
        end
        
    end
%     if mod(iter+1,50) == 0
% %         mod(iter+1,50), iter
%         count_list = [count_list; count];
%     end  
    
end
count, size(result,1)

criticality = 0;
for i = 1:8
    criticality = criticality + (8-i)/7*count(i);
end
criticality/sum(count)

