function [sorted_violation_pattern_list,sorted_pop] = Distance_Violation_Pattern_Ranking (violation_pattern_to_search, population, scores)
sorted_violation_pattern_list = [];
sorted_pop = zeros(size(population,1),size(population,2),size(violation_pattern_to_search,1));
distance = zeros(size(violation_pattern_to_search,1), size(population,1));

for i = 1:size(violation_pattern_to_search,1)
    for j = 1:size(population,1)

% for i = 1:1
%     for j = 1:size(population,1)      
        violation_pattern = violation_pattern_to_search(i,:);
        dist = 0;
        if violation_pattern(1) == 0
            if abs(scores(j,1)) >= 0.8
                dist1 = 0;
            else
                dist1 = 0.8 - abs(scores(j,1));
            end
        else
            if abs(scores(j,1)) < 0.8
                dist1 = 0;
            else
                dist1 = abs(scores(j,1)) - 0.8;
            end
        end
            
        if violation_pattern(2) == 0
            if abs(scores(j,2)) >= 90*1000
                dist2 = 0;
            else
                dist2 = (90*1000 - abs(scores(j,2)))/(100*1000);
            end
        else
            if abs(scores(j,2)) < 90*1000
                dist2 = 0;
            else
                dist2 = (abs(scores(j,2)) - 90*1000)/(100*1000);
            end
        end
        
        if violation_pattern(3) == 0
            if abs(scores(j,3)) <= 5.4*1e6
                dist3 = 0;
            else
                dist3 = (abs(scores(j,3)) - 5.4*1e6)/(5.4*1e6);
            end
        else
            if abs(scores(j,3)) > 5.4*1e6
                dist3 = 0;
            else
                dist3 = (5.4*1e6 - abs(scores(j,3)))/(5.4*1e6);
            end
        end
%         dist1,dist2,dist3
        dist = sqrt(dist1.^2 + dist2.^2 + dist3.^2);
        distance (i,j) = dist; 
    end
end
distance;
dist_mean = mean(distance,2);
dist_rank = [];
for i = 1: length(dist_mean)
    dist_rank = [dist_rank; [i,dist_mean(i)]];
end
sort_dist_rank = sortrows(dist_rank,2);
length(sort_dist_rank)
for i = 1:length(sort_dist_rank)
    index = sort_dist_rank(i,1);
    sorted_violation_pattern_list = [sorted_violation_pattern_list; violation_pattern_to_search(index,:)];
end

distance =  distance';
index_list = 1:1:size(distance,1);
distance_index = [index_list', distance];
for i = 2:size(distance_index,2)
% for i = 2:2
    sort_dist_each_pattern = sortrows(distance_index,i);
    index = sort_dist_each_pattern(:,1);
    for j = 1:size(population,1) 
        sorted_pop (j,:,i-1) = population(index(j),:);
    end
end
