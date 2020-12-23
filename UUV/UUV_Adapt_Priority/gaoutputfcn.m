function [state,options,optchanged] = gaoutputfcn(options,state,flag)
global datafolder
global start_generation
global goal_selection_flag
global goal_round
global priority_list
global violation_pattern_distance
global violation_pattern_relation
global violation_pattern_to_search
global violation_pattern_ranking
global best_pop
optchanged = false;

if state.isFeas
    Pop = [];
    fitness = [];
    [m,n] = size(state.Population);
    for i = 1:m
        for j = 1:floor(n/4)
            Pop(i,(j-1)*4+1) = round(state.Population(i,(j-1)*4+1));
            Pop(i,(j-1)*4+2) = round(state.Population(i,(j-1)*4+2));
            Pop(i,(j-1)*4+3) = round(state.Population(i,(j-1)*4+3));
            if Pop(i,(j-1)*4+3) == 3
                Pop(i,(j-1)*4+4) = 0;
            else
                Pop(i,(j-1)*4+4) =  max(0, state.Population(i,(j-1)*4+4));
            end
        end
        for fun_num = 1:size(state.Score,2)
            fitness(i,fun_num) = state.Score(i,fun_num);
        end
    end
    name =  'interval-results-'+ string(start_generation)+ '.mat';
    path = strcat(datafolder,'/',name);
    save(path,'Pop', 'fitness','goal_selection_flag','violation_pattern_distance','violation_pattern_relation','violation_pattern_to_search','violation_pattern_ranking');

    for i = 1:length(goal_round)
        if start_generation == goal_round(i)
%     if mod (start_generation,goal_round)==0 
            evaluation = [];
            population = []; 
            count = zeros(1,8);
            for k = 1:10000
                name = 'interval-results-' + string(k) + '.mat';
                filename = strcat(datafolder,'/',name);
                if exist(filename,'file')==0
                    break
                end
                data = load(filename);
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
            violation_pattern_to_search = [];
            for i = 1:size(priority_list,1)
                if count(i) == 0
                    violation_pattern_to_search = [violation_pattern_to_search; priority_list(i,:)];
                end
            end

            [violation_pattern_distance, best_pop] = Distance_Violation_Pattern_Ranking (violation_pattern_to_search, population, evaluation);
            violation_pattern_relation = Relation_Violation_Pattern_Ranking (violation_pattern_to_search, goal_selection_flag);

             violation_pattern_ranking =  Ensemble_Ranking(violation_pattern_distance, violation_pattern_relation, violation_pattern_to_search);

            if size(violation_pattern_ranking,1) ~= 0 
                goal_selection_flag = violation_pattern_ranking(1,:);  
            else
                goal_selection_flag = [1,1,1];
            end
        end
    end
    
    start_generation = start_generation + 1;  
end

switch flag
    case 'init'
        disp('Starting the algorithm');
    case {'iter','interrupt'}
        disp('Iterating ...')
    case 'done'
        disp('Performing final task');
end