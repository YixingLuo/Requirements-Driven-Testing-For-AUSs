function sorted_violation_pattern_list = Ensemble_Ranking(violation_pattern_distance, violation_pattern_relation, violation_pattern_to_search)
weights = [1,1,1];
violation_pattern_list = [];
sorted_violation_pattern_list = [];
ranking_list = [];
for i = 1: size(violation_pattern_to_search,1)
    violation_pattern = violation_pattern_to_search (i,:);
    for j = 1: size(violation_pattern_distance,1) 
        if violation_pattern_distance(j,:) == violation_pattern
            for k = 1: size(violation_pattern_relation,1) 
                if violation_pattern_relation(k,:) == violation_pattern                
                    violation_pattern_list = [violation_pattern_list; violation_pattern];
                    rank = i*weights(1) + j*weights(2) + k*weights(3);            
                    ranking_list = [ranking_list;[i , rank]];
                end
            end
        end
    end
end

sorted_rank_list = sortrows(ranking_list,2);
for i = 1: length(sorted_rank_list)
    index = sorted_rank_list(i,1);
    sorted_violation_pattern_list = [sorted_violation_pattern_list; violation_pattern_list(index,:)];
end
    