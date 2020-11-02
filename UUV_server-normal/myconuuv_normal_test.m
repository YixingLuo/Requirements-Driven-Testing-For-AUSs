function [c,ceq] = myconuuv_normal_test(x_initial)
global num_incidents
global pastdistance
global pasttime
global pastenergy
global pastaccuracy
c=[];
ceq=[];
m = num_incidents;
x = [];
% [m,n] = size(x_test);
for i = 1:m
    x(i,1) = round(x_initial((i-1)*4+1));
    x(i,2) = round(x_initial((i-1)*4+2));
    x(i,3) = round(x_initial((i-1)*4+3));
    x(i,4) = x_initial((i-1)*4+4);
end

% for i = 1:m
%     x(i,1) = round(x(i,1));
%     x(i,2) = round(x(i,2));
%     x(i,3) = round(x(i,3));
% end

% for i = 1:m
%     if x(i,2) == 4
%         ceq = [ceq, x(i,4)];
%     elseif x(i,2)== 5 || x(i,2) == 6
%         ceq = [ceq, x(i,3)];
%     else
%         c = [c, -x(i,4)];
%         c = [c, x(i,4)-20];
%     end
% end

for i = 1:m-1
    c = [c, x(i,1)-x(i+1,1)+1];
end

% c = [c, pastdistance - 100*1000];
% c = [c, 5.4*1e6 - pastenergy];

