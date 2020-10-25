function [c,ceq] = myconuuv_NN(x_initial)
global num_incidents
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

XTest = x_initial';
model_name = 'NN_fit_net';
mdl = load(model_name);
Y_preditct = mdl.net(XTest);
for i = 1:3
    c = [c,Y_preditct(i)-1];
    c = [c,-Y_preditct(i)];
end

end

