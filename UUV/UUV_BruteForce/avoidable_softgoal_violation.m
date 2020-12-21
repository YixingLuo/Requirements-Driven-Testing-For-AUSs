%% statics for soft goal violaiton
% count = [];
% i1=[];
% i2=[];
% d1=[];
% d2=[];
% condition = [];
% condition2 = [];
% for i = 1:size(data1,1)
%     if (data2(i,3)>0&&data2(i,3)<=(1-1e-4))||(data2(i,5)>0&&data2(i,5)<=(1-1e-4))
%         count = [count,i];
%         i1 = [i1;index(i,:)];
%         i2 = [i2;index2(i,:)];
%         d1 = [d1;data1(i,:)];
%         d2 = [d2;data2(i,:)];
%     end
% end
% 
% for i = 1:length(count)
%     name = 'condition' + string(count(i));
%     cond = load(name);
%     temp_cond = [];
%     for j = 1:size(i1,2)
%         temp_cond = [temp_cond; [i1(i,j),cond.condition(j,:)]];
%     end
%     condition = [condition; temp_cond];
%     temp_cond = [];
%     for j = 1:size(i2,2)
%         temp_cond = [temp_cond; [i2(i,j),cond.condition(j,:)]];
%     end
%     condition2 = [condition2; temp_cond];
% end

%% establish regression tree
% clc
% clear
% datafolder = 'soft-goal-violation-2';
% datalog_name = strcat(datafolder,'/data20201104T001415','.mat');
% datalog = load(datalog_name);
% cnt = datalog.count;
% num = 1;
% for i = 1:length(cnt)
% % for i = 1:1000
%     count = cnt(i);
%     name = strcat(datafolder,'/condition', string(count),'.mat');
% %     name = strcat(datafolder,'/condition', string(i),'.mat');
% %     name_idx = strcat(datafolder,'/index', string(i),'.mat');
%     if exist(name)
%         cond = load(name);
% %         index = load(name_idx);
%         for j = 1:size(cond.cond,1)
%             X(num,(j-1)*4+1) = cond.cond(j,1);
%             X(num,(j-1)*4+2) = cond.cond(j,2);
%             X(num,(j-1)*4+3) = cond.cond(j,3);
%             X(num,(j-1)*4+4) = cond.cond(j,4);
%         end
%         Y(num,:) = [datalog.data1(count,1), datalog.data1(count,3), datalog.data1(count,5)];
% %         Y(num,:) = [datalog.data1(i,1), datalog.data1(i,3), datalog.data1(i,5)];
%         num = num + 1;      
%     end
% end
% 
% for i = 1:3
%     Mdl = fitrtree(X,Y(:,i),'OptimizeHyperparameters','auto',...
%     'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName',...
%     'expected-improvement-plus'));
% %     model_name = 'Reg_model-all-'+ string(i);
%     model_name = 'Reg_model-vio-'+ string(i);
%     model_name = strcat(datafolder,'/',model_name);
%     save (model_name,'Mdl')
% end

%% prediction error
clc
clear
datafolder = 'soft-goal-violation-2';
datalog_name = strcat(datafolder,'/data20201104T001415','.mat');
datalog = load(datalog_name);


cnt = datalog.count;
num = 1;
% for i = 1:length(cnt)
for i = 1:1000
%     count = cnt(i);
    if ismember(i,cnt)
        continue;
    end
    count = i;
    name = strcat(datafolder,'/condition', string(count),'.mat');
    if exist(name)
        cond = load(name);
        for j = 1:size(cond.cond,1)
            X(num,(j-1)*4+1) = cond.cond(j,1);
            X(num,(j-1)*4+2) = cond.cond(j,2);
            X(num,(j-1)*4+3) = cond.cond(j,3);
            X(num,(j-1)*4+4) = cond.cond(j,4);
        end
        Y(num,:) = [datalog.data1(count,1), datalog.data1(count,3), datalog.data1(count,5)];
        num = num + 1;      
    end
end

sco_predict = [];
sco_raw = [];
model_name = strcat (datafolder , '/Reg_model-vio-1');
mdl1 = load (model_name);
model_name = strcat(datafolder, '/Reg_model-vio-2');
mdl2 = load (model_name);
model_name = strcat(datafolder, '/Reg_model-vio-3');
mdl3 = load (model_name);

num = 1;
% for j = 1:length(cnt)  
for j = 1:1000
    if ismember(j,cnt)
        continue;
    end
    sco_raw(num,:) = Y(num,:);
    sco_predict(num,1) = predict(mdl1.Mdl,X(num,:));
    sco_predict(num,2) = predict(mdl2.Mdl,X(num,:));
    sco_predict(num,3) = predict(mdl3.Mdl,X(num,:));
    num = num+1;
end
% for j = 1:3
%     perf(j) = perform(mdl1.Mdl,sco_raw(:,j), sco_predict(:,j));
% end
data_predict = mean(sco_predict);
data_raw = mean(sco_raw);
for j = 1:3
   train_err = sco_predict(:,j) - sco_raw(:,j);
   n1 = length(sco_raw(:,j));
   train_RMSE(j) = sqrt(sum((train_err).^2)/n1);
end
for j = 1:3
   if j == 1
        partitionedModel = crossval(mdl1.Mdl, 'KFold', 5);
   elseif j == 2
       partitionedModel = crossval(mdl2.Mdl, 'KFold', 5);
   else
       partitionedModel = crossval(mdl3.Mdl, 'KFold', 5);
   end
   validationPredictions = kfoldPredict(partitionedModel);
   validationRMSE(j) = sqrt(kfoldLoss(partitionedModel, 'LossFun', 'mse'));
end


