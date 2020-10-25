clc
clear
global hour
hour  = 1;
global num_incidents
num_incidents = 5; 
global iter
population_size = 500;
total_generation = 300;
iter = 5;
global datafolder
% da = date;
da = fix(datevec(now));
% datafolder = strcat('Datalog-',string(da(1)),'-',string(da(2)),'-',string(da(3)),'-',string(da(4)),'-',string(da(5)), '-Adapt');
% datafolder = strcat('Datalog-',string(da(1)),'-',string(da(2)),'-',string(da(3)),'-',string(da(4)),'-',string(da(5)), '-NN-iter');
datafolder = strcat('Datalog-',string(da(1)),'-',string(da(2)),'-',string(da(3)),'-',string(da(4)),'-',string(da(5)), '-Reg-iter');
mkdir(datafolder);
addpath(datafolder);
global xbest
global ybest
global ReqTarget
global ReqSatFlag
xbest = [];
ybest = [];
ReqTarget = [0.9,1,1];
ReqSatFlag = [0,0,0];
for hour = 1:iter
 
    lb=[];
    ub=[];

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
    options.PopulationSize = population_size;
%     options.Display = 'iter';
%     options.MaxGenerations = floor(total_generation/iter);
    options.MaxGenerations = inf;
    
    % options = optimoptions(options,'CreationFcn',{@gacreationnonlinearfeasible,...
    %     'UseParallel',true,'NumStartPts',20});
    if hour > 1
%         options = optimoptions(options,'CreationFcn',@initialize_variables_adaptive);
%         options = optimoptions(options,'CreationFcn',@initialize_variables_NN);
%         options = optimoptions(options,'CreationFcn',@initialize_variables_NN_iter);
        options = optimoptions(options,'CreationFcn',@initialize_variables_Reg_iter);
    else
        options.CreationFcn = @gacreationnonlinearfeasible;
    end   
    options.OutputFcn = @gaoutputfcn;
%     options.MaxTime = inf;
    options.MaxTime = 360; %% 1 hour
%     options.PlotFcn = @gaplotbestf;

    % Population = initialize_variables(3, @uuv_normal_test, options);

    [x,fval,exitflag,output,population,scores] = gamultiobj(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test,options);
    % [x,fval,exitflag,output,population,scores] = ga(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test)

    time = datestr(now,30);
    name = 'ga-multiobj-adaptive-iter-' + string(iter) + '-'+ string(hour) + '.mat';
    path = strcat(datafolder,'/',name);
    save(path);
    figurename ='ga-multiobj-adaptive-figure-iter-' + string(iter) + '-' + string(hour);
    figpath = strcat(datafolder,'/',figurename);
    savefig(figpath);
    fprintf('UUV_test_adaptive:training ieration %d \n', hour);


end
