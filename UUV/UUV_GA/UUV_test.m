global hour
global num_incidents
global goal_selection_flag
global goal_round
global Scores
global datafolder
global start_generation

for round = 1:1:5
% clc
% clear
% delete(gcp('nocreate'))
% parpool('local')

goal_selection_flag = [1, 1, 1];
goal_round = 50;
Scores = [];
num_incidents = 5; 

da = fix(datevec(now));
datafolder = strcat('Datalog-',string(da(1)),'-',string(da(2)),'-',string(da(3)),'-',string(da(4)),'-',string(da(5)));
mkdir(datafolder);
addpath(datafolder);

% for hour = 1:1:10

start_generation = 0;

total_generation = 100;
hour = 24;
  
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
            lb((i-1)*4+j) = 1-0.5;
            ub((i-1)*4+j) = 5+0.49;           
        else
            lb((i-1)*4+j) = 0;
            ub((i-1)*4+j) = 40;
        end
    end
end


% options.SelectionFcn = 'selectiontournament';
% options.PlotFcn = 'gaplotpareto';
% options = optimoptions('gamultiobj','PlotFcn',@gaplotpareto);
option_temp = load('options.mat');
options = option_temp.options;
options.FunctionTolerance = 0;
options.ConstraintTolerance = 0;
options.PopulationSize = 50;
options.CrossoverFcn = @crossoversinglepoint;
options.CrossoverFraction = 0.8;
options.MaxGenerations = total_generation;
% options.MaxGenerations = inf;
% options.CreationFcn = @initialize_variables;
options.CreationFcn = @gacreationuniform;
options.OutputFcn = @gaoutputfcn;
% options.HybridFcn = {@fgoalattain,[]};
options.MaxTime = hour * 3600;
options.MaxStallGenerations = total_generation; 
% options.UseParallel = true;
options.Display = 'iter';


[x,fval,exitflag,output,population,scores] = gamultiobj(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test,options);
% [x,fval,exitflag,output,population,scores] = ga(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test)

time = datestr(now,30);
% name =  'ga-multiobj-iternum-'+ string(total_generation)+ '.mat';
name =  'ga-multiobj-iternum-'+ string(start_generation)+ '.mat';
path = strcat(datafolder,'/',name);
save(path);
% figurename =  'ga-multiobj-figure-iternum-' + string(total_generation);
figurename =  'ga-multiobj-figure-iternum-' + string(start_generation);
figpath = strcat(datafolder,'/',figurename);
savefig(figpath);
fprintf('UUV_test: iteration number %d, Time is %s \n', start_generation, string(time));


% hour = hour + 1;
end