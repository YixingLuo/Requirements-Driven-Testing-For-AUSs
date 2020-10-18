clc
clear
for hour = 2:4:24
global num_incidents
num_incidents = 5;    
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
options.PopulationSize = 500;
% options = optimoptions(options,'CreationFcn',{@gacreationnonlinearfeasible,...
%     'UseParallel',true,'NumStartPts',20});
options = optimoptions(options,'CreationFcn',@initialize_variables);
% rng default
% x = ga(fun,nvars,A,b,Aeq,beq,lb,ub,nonlcon,IntCon,options)
options.MaxTime = 3600 * hour;

% Population = initialize_variables(3, @uuv_normal_test, options);

[x,fval,exitflag,output,population,scores] = gamultiobj(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test,options);
% [x,fval,exitflag,output,population,scores] = ga(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test)

time = datestr(now,30);
name =  string(time) + '-' + 'ga-multiobj-'+ string(hour) + '.mat';
save(name);
figurename =  string(time) + '-' + 'ga-multiobj-figure-' + string(hour);
savefig(figurename);
fprintf('UUV_test:training hour %d, Time is %s \n', hour, string(time));

% for i = 1:size(x,1)
% m = num_incidents;
% for i = 1:m
%     x_last(i,1) = round(x((i-1)*4+1));
%     x_last(i,2) = round(x((i-1)*4+2));
%     x_last(i,3) = round(x((i-1)*4+3));
%     x_last(i,4) = x((i-1)*4+4);
% end
% x_last
% for i = 1:m
%     x_last(i,1) = x((i-1)*4+1);
%     x_last(i,2) = x((i-1)*4+2);
%     x_last(i,3) = x((i-1)*4+3);
%     x_last(i,4) = x((i-1)*4+4);
% end
% x_last
% end
end