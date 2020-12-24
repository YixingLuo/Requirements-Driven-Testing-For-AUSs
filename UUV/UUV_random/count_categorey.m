[m,n] = size(data1);
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

for i = 1:1:m
    temp_result = data1(i,:);
    flag = zeros(1,3);
    if abs(temp_result(2)) < 0.9*0.9
        flag(1) = 1;
    end
    if abs(temp_result(4)) < 100*0.99*1000 
        flag(2) = 1;
    end
    if abs(temp_result(6)) > 5.4*1.001*1e6
        flag(3) = 1;
    end
    result = [result; flag];
    for j = 1:size(priority_list,1)
        if priority_list(j,:) == flag
            count(j) = count(j) + 1;
            break
        end
    end
end
count, size(result,1)

criticality = 0;
for i = 1:8
    criticality = criticality + (8-i)/7*count(i);
end
criticality/sum(count)
