size = 1000;
data1_copy = [];
data1_copy = data1 (1:size,:);
for i = 1:2:5
    for j = 1:size
        if data1_copy(j,i)>1
            data1_copy(j,i) = 1;
        end
    end
end
data1_sorted = [];
for i = 1:6
    data1_sorted(:,i) = sort(data1_copy(:,i));
end
data1_mean = [];
for i = 1:5
    data1_mean(i,:) = mean(data1_sorted(1+5*(5-i):size-5*(5-i),:));
end
%% risk
data1_risk = [];
% data1_copy (:,1) = data1_copy(:,end);
for i = 1:2:5
    for j = 1:size
        if data1_copy(j,i)>= 0.95
            data1_risk(j,ceil(i/2)) = 1;
        else
            data1_risk(j,ceil(i/2)) = 0;
        end
    end
end
data1_risk_sorted = [];
for i = 1:3
    data1_risk_sorted(:,i) = sort(data1_risk(:,i));
end
data1_risk_mean = [];
for i = 1:5
    data1_risk_mean(i,:) = mean(data1_risk_sorted(1+5*(5-i):size-5*(5-i),:));
end


data1_achievement = [0,0,0,0];
for i = 1:size
    j =  data1_risk(i,1) + data1_risk(i,2) + data1_risk(i,3);
    data1_achievement(j+1) = data1_achievement(j+1) +1;  
end
data1_achievement = flip(data1_achievement');
