[m,n] = size(data1);
result = [];
count = zeros(1,8);

for i = 1:1:m
    temp_result = data1(m,:);
    flag = zeros(1,3);
    if temp_result(2)<0.9
        flag(1) = 1;
    end
    if temp_result(4)< 100*1000
        flag(2) = 1;
    end
    if temp_result(6)>5.4*1e6
        flag(3) = 1;
    end
    result = [result; flag];
    sum = flag(1)*2^0 + flag(2)*2^1 + flag(3)*2^2;
    if sum > 0
        count(sum) = count(sum) + 1;
    end
end
count