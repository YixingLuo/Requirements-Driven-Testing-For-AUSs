function Population = initialize_variables_NN(GenomeLength, uuv_normal_test, options)
Population = [];
totalpopulation = sum(options.PopulationSize);
global num_incidents
global uuv
global hour
global iter
global datafolder
if hour == 1
    for pop = 1:1:totalpopulation
    uuv = UnmannedUnderwaterVehicle();
    l = 1:1:15;
    disturb = randi([1,4],1,l(num_incidents));
    a=2:359;
    K=randperm(length(a));
    N=length(disturb);
    index1 = a(K(1:N));
    % index1 = randperm(359,length(disturb));
    index = sort(index1);
    condition = [];
    failure_list = [];
        for i = 1: length(disturb)
            if disturb(i) == 1
                idx = unidrnd(5);   
                acc_ratio = unidrnd(100);
                acc = uuv.s_accuracy(idx)*acc_ratio/100;
                condition(i,:) = [1,idx,acc];
            elseif disturb(i) == 2
                idx = unidrnd(5);
                energy_ratio = 100 + unidrnd(100);
                energy = uuv.s_energy(idx)*energy_ratio/100;
                condition(i,:) = [2,idx,energy];
           elseif disturb(i) == 3
                idx = unidrnd(5);
                speed_ratio = unidrnd(100);
                speed = uuv.s_speed(idx)*speed_ratio/100;
                condition(i,:) = [3,idx,speed];   
            elseif disturb(i) == 4
                idx = unidrnd(5);
                if any (idx == failure_list)
                    idx = unidrnd(5);
                end
                condition(i,:) = [4,idx,-1];
            end
        end
        x_test_initial = [];
        for i = 1: length(disturb)
    %         x0(i,1) = index (i);
    %         x0(i,2) = condition(i,1);
    %         x0(i,3) = condition(i,2);
    %         x0(i,4) = condition(i,3);
            x_test_initial((i-1)*4+1) = index (i);
            x_test_initial((i-1)*4+2) = condition(i,1);
            x_test_initial((i-1)*4+3) = condition(i,2);
            x_test_initial((i-1)*4+4) = condition(i,3);
        end
%         f  = uuv_normal_test(x_test_initial);
        Population(pop,1:4*num_incidents) =  x_test_initial;
    %     for fit = 1:1:3
    %         Population(pop,fit+4*num_incidents)=f(fit);
    %     end
    end
elseif hour > 1
    model_num = hour-1;
    Population = [];
    for model_index = 1:model_num
        name = 'ga-multiobj-adaptive-iter-' + string(iter) + '-'+ string(model_index) + '.mat';
        pre_result_name = strcat(datafolder,'/',name);
        pre_result = load(pre_result_name);
        Population = [Population;pre_result.population];
    end
    [m,n] = size(Population);
    for i = 1:m
        for j = 1:num_incidents
            Population(i,(j-1)*4+1) = round(Population(i,(j-1)*4+1));
            Population(i,(j-1)*4+2) = round(Population(i,(j-1)*4+2));
            Population(i,(j-1)*4+3) = round(Population(i,(j-1)*4+3));
            Population(i,(j-1)*4+4) = Population(i,(j-1)*4+4);
        end
%         Y(i)=pre_result.scores(i,1)*2^0+pre_result.scores(i,2)*2^1+pre_result.scores(i,3)*2^2;    
        Y(i,1)=pre_result.scores(i,1);
        Y(i,2)=pre_result.scores(i,2);
        Y(i,3)=pre_result.scores(i,3);
    end
    X = Population;
    
    X=X';
    Y=Y';
    hiddenLayerSize = 10;
    net = fitnet(hiddenLayerSize);
    net.divideParam.trainRatio = 70/100;
    net.divideParam.valRatio = 15/100;
    net.divideParam.testRatio = 15/100;
    net.trainParam.epochs = 300;
    net.trainParam.goal = 1e-6;
    [net,tr] = train(net,X,Y); 
    
    model_name = 'NN_fit_net'+ string(iter) + '-'+ string(model_num);
    model_name = strcat(datafolder,'/',model_name);
    save (model_name,'net')
    fprintf('UUV_test_adaptive:generating the requirements violaiton predictior %d \n', model_num);
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
    options_new.PopulationSize = totalpopulation;
    options_new.InitialPopulationMatrix = Population;
    [x_new,fval_new,exitflag_new,output_new,population_new,scores_new] = gamultiobj(@NNPredict_UUV,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test,options_new);
%     [x,fval,exitflag,output,population,scores] = gamultiobj(@uuv_normal_test,4*num_incidents,[],[],[],[],lb,ub,@myconuuv_normal_test,options);
    [m,n] = size(population_new);
    for i = 1:m
        for j = 1:num_incidents
            Population(i,(j-1)*4+1) = round(population_new(i,(j-1)*4+1));
            Population(i,(j-1)*4+2) = round(population_new(i,(j-1)*4+2));
            Population(i,(j-1)*4+3) = round(population_new(i,(j-1)*4+3));
            Population(i,(j-1)*4+4) = population_new(i,(j-1)*4+4);
        end
    end
   population_name = strcat(datafolder,'/','Initial-Population-iter-'+string(iter)+'-'+string(hour));
   save(population_name,'Population');
   fprintf('UUV_test_adaptive:generating the the initial population %d \n', iter);
end
end

