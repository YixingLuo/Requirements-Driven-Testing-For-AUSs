% clc
% clear
result = [];
count = zeros(1,8);
count_list = [];
priority_list = [1,1,1; 
                 0,1,1;
                 1,0,1;
                 1,1,0;
                 0,0,1;
                 0,1,0;
                 1,0,0;
                 0,0,0;];

for iter = 1:1:400
    filename = 'Datalog-2020-12-23-12-8/interval-results-' + string(iter) + '.mat';
    if exist(filename,'file')==0
        count_list = [count_list; count];
        break
    end
    
    data = load(filename);
        
    data1 = data.fitness;
    [m,n] = size(data1);
    for i = 1:1:m
        temp_result = data1(i,:);
        goal_flag = zeros(1,3);
        if abs(temp_result(1))< 0.8
            goal_flag(1) = 1;
        end
        if abs(temp_result(2))< 90*1000
            goal_flag(2) = 1;
        end
        if abs(temp_result(3))> 5.4*1e6
            goal_flag(3) = 1;
        end
%         count(sum) = count(sum) + 1;
        for j = 1:size(priority_list,1)
            if priority_list(j,:) == goal_flag
%                 goal_flag, priority_list(j,:),j
                count(j) = count(j) + 1;
                break
            end
        end
    end
    if mod(iter,50) == 0
%         mod(iter+1,50), iter
        count_list = [count_list; count];
    end  
    
end

% count_list, size(result,1)
count_list, count
% start_generation = 50;
% goal_round = 50;
% if mod (start_generation,goal_round)==0 
%     start = 1;
%     for i = 1:size(priority_list,1)
%         if count(i) == 0
%             start = i
%             break;
%         end
%     end
% goal_selection_flag = priority_list(start,:)    
% end