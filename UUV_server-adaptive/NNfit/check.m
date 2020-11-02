% sco = [];
% for i = 1:500
%     sco(i,:) = uuv_normal_test(Population(i,:));
% %     input =  Population(i,:)';
% %     sco(i,:) = net(input);
% %     if  sco(1) ~= scores(i,1) || sco(2) ~= scores(i,2) || sco(3) ~= scores(i,3)
% %         i,sco,scores(i,:)
% %         sco(1)-scores(i,1), sco(2)-scores(i,2),sco(3)-scores(i,3)
% % %         mse(sco,scores(i,:))
% %     end
% end
% data = mean(sco);


data_predict = [];
data_raw = [];
for i = 1:9
    sco_predict = [];
    sco_raw = [];
    model_name = 'Datalog-2020-10-25-0-8-NN-iter\NN_fit_net10-'+string(i);
    mdl = load (model_name);
    pop_name = 'Datalog-2020-10-25-0-8-NN-iter\Initial-Population-iter-10-'+string(i+1);
    Pop = load(pop_name);
    for j = 1:500     
        sco_raw(j,:) = uuv_normal_test(Pop.Population(j,:));
        sco_predict(j,:) = mdl.net(Pop.Population(j,:)'); 
    end
   perf(i) = perform(mdl.net,sco_raw, sco_predict);
   data_predict(i,:) = mean(sco_predict);
   data_raw(i,:) = mean(sco_raw);
end

% sco = [];
% for i = 1:500
%     sco (i,:)= net(population(i,:)');
% %     if  sco ~= scores(i,:)
% %         i,sco,scores(i,:)
% %     end    
% end
% mse(sco,scores)
% mean(sco)
% meanr(scores)
% 
% sco = [];
% scores = [];
% for i = 1:500
%     sco (i,:)= net(Population(i,:)'); 
%     scores (i,:)= uuv_normal_test(Population(i,:));
% end
% mse(sco,scores)
% mean(sco)
% mean(scores)

%     [m,n] = size(population);
%     for i = 1:m
% %         for j = 1:num_incidents
% %             population(i,(j-1)*4+1) = round(population(i,(j-1)*4+1));
% %             population(i,(j-1)*4+2) = round(population(i,(j-1)*4+2));
% %             population(i,(j-1)*4+3) = round(population(i,(j-1)*4+3));
% %             population(i,(j-1)*4+4) = population(i,(j-1)*4+4);
% %         end 
%         Y(i,1)=scores(i,1);
%         Y(i,2)=scores(i,2);
%         Y(i,3)=scores(i,3);
%     end
%     
%     X = population;
%     
%     
%     X=X';
%     Y=Y';
%     hiddenLayerSize = 20;
%     net = fitnet([20,10],'trainbr');
%     net.divideParam.trainRatio = 70/100;
%     net.divideParam.valRatio = 15/100;
%     net.divideParam.testRatio = 15/100;
%     net.trainParam.epochs = 500;
%     net.trainParam.goal = 1e-6;
%     [net,tr] = train(net,X,Y); 
%     outputs = net(X);
%     errors = gsubtract(outputs,Y);
%     performance = perform(net,Y,outputs)
% %     figure, plotperform(tr)
% %     figure, plottrainstate(tr)
% %     % figure, plotfit(targets,outputs)
% %     figure, plotregression(Y,outputs)
% %     figure, ploterrhist(errors)
%     
%     model_name = 'NN_fit_net';
%     model_name = strcat(model_name);
%     save (model_name,'net','tr')

%     lb=[];
%     ub=[];
%     for i = 1:num_incidents
%         for j = 1:4
%             if j == 1 %% index
%                 lb((i-1)*4+j) = 1+i-0.5;
%                 ub((i-1)*4+j) = 256+i+0.49;
%             elseif j == 2 %% conditon_no
%                 lb((i-1)*4+j) = 1-0.5;
%                 ub((i-1)*4+j) = 4+0.49;
%             elseif j == 3 %% sensor_no
%                 lb((i-1)*4+j) = 1-0.5;
%                 ub((i-1)*4+j) = 5+0.49;
%             else
%                 lb((i-1)*4+j) = -1;
%                 ub((i-1)*4+j) = 2;
%             end
%         end
%     end
%     option_temp = load('options.mat');
%     options_new = option_temp.options;
%     options_new.PopulationSize = 500;
%     options_new.InitialPopulationMatrix = population;
%     options_new.FunctionTolerance = 1e-6;
%     options_new.ConstraintTolerance = 1e-6;
%     options_new.MaxTime = 3600; %% 1 hour
%     options_new.MaxGenerations = 10;
% %     options_new.Display = 'iter';
%     [x_new,fval_new,exitflag_new,output_new,population_new,scores_new] = gamultiobj(@NNPredict,4*num_incidents,[],[],[],[],lb,ub,@ myconuuv_NN,options_new);
% 
% function f = NNPredict(XTest) %#codegen
% [m,n] = size(XTest);
% for i = 1:m
%     for j = 1:5
%         XTest(i,(j-1)*4+1) = round(XTest(i,(j-1)*4+1));
%         XTest(i,(j-1)*4+2) = round(XTest(i,(j-1)*4+2));
%         XTest(i,(j-1)*4+3) = round(XTest(i,(j-1)*4+3));
%         XTest(i,(j-1)*4+4) = XTest(i,(j-1)*4+4);
%     end
% end
% XTest = XTest';
% model_name = 'NN_fit_net';
% mdl = load(model_name);
% % size(XTest)
% Y_preditct = mdl.net(XTest);
% % Y_preditct = float(Y_preditct);
% f = Y_preditct;
% end