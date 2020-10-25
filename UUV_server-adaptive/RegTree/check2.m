%     X = xbest;
%     Y = ybest;
%     
%     for i = 1:3
%         Mdl = fitrtree(X,Y(:,i),'OptimizeHyperparameters','auto',...
%         'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName',...
%         'expected-improvement-plus'));
%         model_name = 'Reg_model-'+ string(i);
%         save (model_name,'Mdl')
%     end
    
    %% initial population generation
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
    option_temp = load('options.mat');
    options_new = option_temp.options;
    options_new.PopulationSize = 500;
    options_new.InitialPopulationMatrix = xbest;
    options_new.FunctionTolerance = 0;
    options_new.ConstraintTolerance = 0;
    options_new.MaxGenerations = 100;
%     options_new.Display = 'iter';
    [x_new,fval_new,exitflag_new,output_new,population_new,scores_new] = gamultiobj(@RegPredict_UUV,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test,options_new);
