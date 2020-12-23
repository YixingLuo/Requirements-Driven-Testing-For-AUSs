function sorted_violation_pattern_list = Relation_Violation_Pattern_Ranking (violation_pattern_to_search, goal_selection_flag)
global parent_list
global child_list
global priority_list
sorted_violation_pattern_list = [];
% reward_0 = 1;
gamma = 0.5;
reward = zeros(1,size(priority_list,1));
goal_num = size(violation_pattern_to_search,2);
initial_class = sum(goal_selection_flag);
total_pattern_number = size(priority_list,1);

for i = 1:size(priority_list,1)
    if priority_list(i,:) == goal_selection_flag
        goal_selection_flag_index = i;
        reward_0 = 1;
        reward(goal_selection_flag_index) = reward_0;
        break
    end
end
for i = 1:size(violation_pattern_to_search,1)
    if violation_pattern_to_search(i,:) == goal_selection_flag
        reward_0 = -1;
        reward(goal_selection_flag_index) = reward_0;
        break
    end
end
% reward(goal_selection_flag_index), goal_selection_flag_index
clear sum
count_violation = sum(priority_list,2);
for i = 1:size(priority_list,1)

    ancessor_list = [];
    father_index = [];
    for k = 1:size(parent_list,2)
        if parent_list(i,k) == 1
            father_index = [father_index, k];
        end
    end
    for k = 1:length(father_index)
        ancessor_list = [ancessor_list; priority_list(father_index(k),:)];
    end
%     ancessor_list
    if i == goal_selection_flag_index
        continue
    end

    if isempty(father_index)
        same_pattern = 0;
        reward(i) = 0;
    else
        same_pattern = 0;
        for j = 1:length(father_index)
            for k = 1:size(violation_pattern_to_search,1)
                if priority_list(father_index(j),:) == violation_pattern_to_search(k,:)
                    same_pattern = same_pattern + 1;
                end
            end
        end       
        reward(i) = (length(father_index)-same_pattern)/length(father_index); %% possibility to find
    end
    if count_violation(i) < initial_class %% successor of the current search pattern
        reward(i) = reward(i) + reward_0 * gamma^(initial_class-count_violation(i));
    end
end
    

reward =  reward';
index_list = 1:1:size(reward,1);
reward_list=[];

for i = 1:size(priority_list,1)
    for j = 1:size(violation_pattern_to_search,1)
        if priority_list(i,:) == violation_pattern_to_search(j,:)
            reward_list = [reward_list; [j,reward(i)]];
            break
        end
    end
end
sort_reward = sortrows(reward_list,2,'descend');
for i = 1:size(sort_reward,1)
    sorted_violation_pattern_list = [sorted_violation_pattern_list; violation_pattern_to_search(sort_reward(i),:)];
end
