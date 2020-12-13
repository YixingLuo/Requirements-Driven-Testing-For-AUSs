clc
clear
% delete(gcp('nocreate'))
% parpool('local')
global hour
global num_incidents
num_incidents = 5; 
global datafolder
da = fix(datevec(now));
datafolder = strcat('Datalog-',string(da(1)),'-',string(da(2)),'-',string(da(3)),'-',string(da(4)),'-',string(da(5)));
mkdir(datafolder);
addpath(datafolder);

% for hour = 1:1:10
global start_generation
start_generation = 0;

total_generation = 200;
hour = 24;
% while hour <= 2
  
lb=[];
ub=[];


for i = 1:num_incidents
    for j = 1:4
        if j == 1 %% index
            lb((i-1)*4+j) = 1+i-0.5;
            ub((i-1)*4+j) = 256+i+0.49;
        elseif j == 2 %% conditon_no
            lb((i-1)*4+j) = 1-0.5;
%             ub((i-1)*4+j) = 6+0.49;
            ub((i-1)*4+j) = 4+0.49;
        elseif j == 3 %% sensor_no
            lb((i-1)*4+j) = 1;
            ub((i-1)*4+j) = 5;           
        else
            lb((i-1)*4+j) = 0;
            ub((i-1)*4+j) = 20;
        end
    end
end


% options.SelectionFcn = 'selectiontournament';
% options.PlotFcn = 'gaplotpareto';
% options = optimoptions('gamultiobj','PlotFcn',@gaplotpareto);
option_temp = load('options.mat');
options = option_temp.options;
options.FunctionTolerance = 1e-3;
options.ConstraintTolerance = 1e-3;
options.PopulationSize = 50;
options.CrossoverFcn = @crossoversinglepoint;
options.CrossoverFraction = 0.6;
options.MaxGenerations = total_generation;
% options.MaxGenerations = inf;
options.CreationFcn = @initialize_variables;
% options.CreationFcn = @gacreationnonlinearfeasible;
options.OutputFcn = @gaoutputfcn;
% options.HybridFcn = {@fgoalattain,[]};
% rng default
% x = ga(fun,nvars,A,b,Aeq,beq,lb,ub,nonlcon,IntCon,options)
options.MaxTime = hour * 3600;
% options.UseParallel = true;
options.Display = 'iter';
% options = optimoptions('gamultiobj','UseParallel', true, 'UseVectorized', false);
% Population = initialize_variables(3, @uuv_normal_test, options);

[x,fval,exitflag,output,population,scores] = gamultiobj(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test,options);
% [x,fval,exitflag,output,population,scores] = ga(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test)

time = datestr(now,30);
% name =  'ga-multiobj-iternum-'+ string(total_generation)+ '.mat';
name =  'ga-multiobj-iternum-'+ string(hour)+ '.mat';
path = strcat(datafolder,'/',name);
save(path);
% figurename =  'ga-multiobj-figure-iternum-' + string(total_generation);
figurename =  'ga-multiobj-figure-iternum-' + string(hour);
figpath = strcat(datafolder,'/',figurename);
savefig(figpath);
fprintf('UUV_test: iteration number %d, Time is %s \n', hour, string(time));


% hour = hour + 1;
% end