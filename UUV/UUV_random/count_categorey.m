[m,n] = size(data1);
result = [];
count = zeros(1,8);

for i = 1:1:m
    temp_result = data1(i,:);
    flag = zeros(1,3);
    if abs(temp_result(2)) < 0.9
        0.9 - temp_result(2);
        flag(1) = 1;
    end
    if abs(temp_result(4)) < 100*1000 
        100*1000 - temp_result(4);
        flag(2) = 1;
    end
    if temp_result(6) > 5.4*1e6
        temp_result(6) - 5.4*1e6;
        flag(3) = 1;
    end
    result = [result; flag];
    violation_pattern = flag(1)*2^0 + flag(2)*2^1 + flag(3)*2^2 + 1;
    if violation_pattern > 0
        count(violation_pattern) = count(violation_pattern) + 1;
    end
end
count, sum(count)

criticality = 0;
for i = 1:8
    criticality = criticality + (i-1)/7*count(i);
end
criticality/sum(count)
