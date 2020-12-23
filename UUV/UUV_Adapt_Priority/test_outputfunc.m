
global datafolder
global start_generation
global goal_selection_flag
global goal_round
global priority_list
global violation_pattern_distance
global violation_pattern_relation
global violation_pattern_to_search
global parent_list
global child_list
[parent_list, child_list] = Relation(priority_list);

priority_list = [1,1,1; 
                 0,1,1;
                 1,0,1;
                 1,1,0;
                 0,0,1;
                 0,1,0;
                 1,0,0;
                 0,0,0;];
             
        evaluation = [];
        population = []; 
        count = zeros(1,8);
        for k = 1:50
            name = 'Datalog-2020-12-22-20-49/interval-results-' + string(k) + '.mat';
%             filename = strcat(datafolder,'/',name);
            if exist(name,'file')==0
                break
            end
            data = load(name);
            data1 = data.fitness;
            evaluation = [evaluation; data.fitness];
            population = [population; data.Pop];
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
                for j = 1:size(priority_list,1)
                    if priority_list(j,:) == goal_flag
                        count(j) = count(j) + 1;
                        break
                    end
                end
            end
        end
        count;
        violation_pattern_to_search = [];
        for i = 1:size(priority_list,1)
            if count(i) == 0
                violation_pattern_to_search = [violation_pattern_to_search; priority_list(i,:)];
            end
        end
        violation_pattern_to_search;
        [violation_pattern_distance, sorted_pop] = Distance_Violation_Pattern_Ranking (violation_pattern_to_search, population, evaluation);
        violation_pattern_relation = Relation_Violation_Pattern_Ranking (violation_pattern_to_search, goal_selection_flag);

        violation_pattern_ranking = Ensemble_Ranking(violation_pattern_distance, violation_pattern_relation, violation_pattern_to_search);
        
        if size(violation_pattern_ranking,1) ~= 0 
            goal_selection_flag = violation_pattern_ranking(1,:);  
        else
            goal_selection_flag = [1,1,1];
        end
%     end
violation_pattern_to_search,violation_pattern_distance,violation_pattern_relation,violation_pattern_ranking
      