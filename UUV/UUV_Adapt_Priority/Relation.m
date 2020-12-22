function [parent_list, child_list] = Relation(priority_list)

priority_list = [1,1,1; 
                 0,1,1;
                 1,0,1;
                 1,1,0;
                 0,0,1;
                 0,1,0;
                 1,0,0;
                 0,0,0;];
goal_num = size(priority_list,2);
parent_list = zeros(size(priority_list,1),size(priority_list,1));
child_list = zeros(size(priority_list,1),size(priority_list,1));
for i = 1:size(priority_list,1)
    father = priority_list(i,:);
    for j = 1:size(priority_list,1)
        child = priority_list(j,:);
        count_same = 0;
        large_flag = 0;
        for k = 1:goal_num
            if father(k) == child(k)
                count_same = count_same + 1;
            elseif father(k) > child(k)
                large_flag = 1;
            end
        end
        
        if (count_same == goal_num - 1) && large_flag == 1
            parent_list(j,i) = 1;
            child_list(i,j) = 1;
        end
    end
end