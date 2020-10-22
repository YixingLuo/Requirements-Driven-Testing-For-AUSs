clc
clear
global hour
hour  = 10;
total_generation = 2000;
global num_incidents
num_incidents = 5; 
global datafolder
da = fix(datevec(now));
datafolder = strcat('Datalog-',string(da(1)),'-',string(da(2)),'-',string(da(3)),'-',string(da(4)),'-',string(da(5)));
mkdir(datafolder);
addpath(datafolder);

% while hour <= 2
  
lb=[];
ub=[];
% for i = 1:num_incidents
%     for j = 1:4
%         if j == 1 %% index
%             lb(i,j) = 1+i-0.5;
%             ub(i,j) = 256+i+0.49;
%         elseif j == 2 %% conditon_no
%             lb(i,j) = 1-0.5;
%             ub(i,j) = 4+0.49;
%         elseif j == 3 %% sensor_no
%             lb(i,j) = 1-0.5;
%             ub(i,j) = 5+0.49;
%         else
%             lb(i,j) = -1;
%             ub(i,j) = 2;
%         end
%     end
% end

for i = 1:num_incidents
    for j = 1:4
        if j == 1 %% index
            lb((i-1)*4+j) = 1+i-0.5;
            ub((i-1)*4+j) = 256+i+0.49;
        elseif j == 2 %% conditon_no
            lb((i-1)*4+j) = 1-0.5;
            ub((i-1)*4+j) = 4+0.49;
        elseif j == 3 %% sensor_no
            lb((i-1)*4+j) = 1-0.5;
            ub((i-1)*4+j) = 5+0.49;
        else
            lb((i-1)*4+j) = -1;
            ub((i-1)*4+j) = 2;
        end
    end
end

% options.PopulationSize = 500;
% options.SelectionFcn = 'selectiontournament';
% options.PlotFcn = 'gaplotpareto';
% options = optimoptions('gamultiobj','PlotFcn',@gaplotpareto);
option_temp = load('options.mat');
options = option_temp.options;
options.FunctionTolerance = 0;
options.ConstraintTolerance = 0;
options.PopulationSize = 500;
options.MaxGenerations = total_generation;
% options = optimoptions(options,'CreationFcn',{@gacreationnonlinearfeasible,...
%     'UseParallel',true,'NumStartPts',20});
% options = optimoptions(options,'CreationFcn',@initialize_variables);
options.CreationFcn = @gacreationnonlinearfeasible;
% rng default
% x = ga(fun,nvars,A,b,Aeq,beq,lb,ub,nonlcon,IntCon,options)
options.MaxTime = inf;

% Population = initialize_variables(3, @uuv_normal_test, options);

[x,fval,exitflag,output,population,scores] = gamultiobj(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test,options);
% [x,fval,exitflag,output,population,scores] = ga(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test)

time = datestr(now,30);
name =  string(time) + '-ga-multiobj-iternum-'+ string(total_generation)+ '.mat';
save(strcat(datafolder,'/',name));
figurename =  string(time) + '-ga-multiobj-figure-iternum-' + string(total_generation);
savefig(strcat(datafolder,'/',figurename));
fprintf('UUV_test: iteration number %d, Time is %s \n', total_generation, string(time));


% hour = hour + 1;
% end