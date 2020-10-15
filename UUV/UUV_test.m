k=10;    
lb=[];
ub=[];
for i = 1:k
    for j = 1:4
        if j == 1 %% index
            lb(i,j) = 1+i-0.5;
            ub(i,j) = 256+i+0.49;
        elseif j == 2 %% conditon_no
            lb(i,j) = 1-0.5;
            ub(i,j) = 4+0.49;
        elseif j == 3 %% sensor_no
            lb(i,j) = 1-0.5;
            ub(i,j) = 5+0.49;
        else
            lb(i,j) = -1;
            ub(i,j) = 2;
        end
    end
end
x0 = randomsituation_test(k);

options.Algorithm = 'sqp'; 
options.Display = 'off';

% [x,fval,exitflag]=fmincon(@uuv_normal_test,x0,[],[],[],[],lb,ub,@myconuuv_normal_test,options)

rng default
nvars = 2;
opts = optimoptions(@uuv_normal_test,'UseVectorized',true,'PlotFcn','gaplotpareto');
[xga,fvalga,~,gaoutput] = gamultiobj(@(x)mymulti3(x),nvars,[],[],[],[],[],[],[],opts);

% [condition, indextemp] = randomsituation(num,k);
% index(num,:) = indextemp;
% 
% iter = mod(num,iternum);
% if iter == 0
%     iter = iternum;
% end
% data = zeros(1,6);
% [data,usage_plan,planning_time] = uuv_normal(num, indextemp);