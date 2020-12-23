clc
clear

% global goal_scores
% global scenario_pop
global goal_round
global hour
global num_incidents
global goal_selection_flag
global datafolder
global start_generation
global priority_list

priority_list = [1,1,1; 
                 0,1,1;
                 1,0,1;
                 1,1,0;
                 0,0,1;
                 0,1,0;
                 1,0,0;
                 0,0,0;];
global violation_pattern_to_search
violation_pattern_to_search = priority_list;
goal_selection_flag = violation_pattern_to_search(1,:);
global violation_pattern_distance
global violation_pattern_relation
global violation_pattern_ranking
global parent_list
global child_list
[parent_list, child_list] = Relation(priority_list);
violation_pattern_distance = [];
violation_pattern_relation = [];
violation_pattern_ranking = [];
global initial_ratio
global best_pop
best_pop = [];

initial_ratio = 0.5;
% goal_round = [100,200,300,400];
goal_round = [50,100,150,200];

goal_scores = [];
scenario_pop = [];
num_incidents = 5; 

da = fix(datevec(now));
datafolder = strcat('Datalog-',string(da(1)),'-',string(da(2)),'-',string(da(3)),'-',string(da(4)),'-',string(da(5)));
mkdir(datafolder);
addpath(datafolder);
start_generation = 1;
total_generation = 200;
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
            ub((i-1)*4+j) = 20;
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
options.CreationFcn = @initialize_variables;
% options.CreationFcn = @gacreationuniform;
options.OutputFcn = @gaoutputfcn;
% options.HybridFcn = {@fgoalattain,[]};
% rng default
% x = ga(fun,nvars,A,b,Aeq,beq,lb,ub,nonlcon,IntCon,options)
options.MaxTime = hour * 3600;
% options.UseParallel = true;
options.Display = 'iter';
options.MaxStallGenerations = inf;
% options = optimoptions('gamultiobj','UseParallel', true, 'UseVectorized', false);
% Population = initialize_variables(3, @uuv_normal_test, options);

[x,fval,exitflag,output,population,scores] = gamultiobj(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test,options);
% [x,fval,exitflag,output,population,scores] = ga(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test)

time = datestr(now,30);
% name =  'ga-multiobj-iternum-'+ string(total_generation)+ '.mat';
name =  'ga-multiobj-iternum-'+ string(goal_round(end))+ '.mat';
path = strcat(datafolder,'/',name);
save(path);
% figurename =  'ga-multiobj-figure-iternum-' + string(total_generation);
figurename =  'ga-multiobj-figure-iternum-' + string(goal_round(end));
figpath = strcat(datafolder,'/',figurename);
savefig(figpath);
fprintf('UUV_test: iteration number %d, Time is %s \n', goal_round, string(time));


% hour = hour + 1;
% end