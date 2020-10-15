function [c,ceq] = myconuuv_normal_test(x)
c=[];
ceq=[];

[m,n] = size(x);

for i = 1:m
    x(i,1) = round(x(i,1));
    x(i,2) = round(x(i,2));
    x(i,3) = round(x(i,3));
end

for i = 1:m
    if x(i,2) == 2
        c = [c, -x(i,4)+1];
        c = [c, x(i,4)-2];
    elseif x(i,2 == 4)
        ceq = [ceq, x(i,4)+1];
    else
        c = [c, -x(i,4)];
        c = [c, x(i,4)-1];
    end
end

for i = 1:m-1
    c = [c, x(i,1)-x(i+1,1)+1];
end

