clc;
clear;
X=[];
Y=[];
% data_name = 'ga-multiobj-1-20201016T100507.mat';
% data_name = 'ga-multiobj-10-20201018T143659.mat';
data_name = 'Datalog-2020-10-24-12-22-NN-iter\ga-multiobj-adaptive-iter-10-1.mat';
data = load(data_name);
[m,n] = size(data.population);
for i = 1:1:m
    for j = 1:5
        X(i,(j-1)*4+1) = round(data.population(i,(j-1)*4+1));
        X(i,(j-1)*4+2) = round(data.population(i,(j-1)*4+2));
        X(i,(j-1)*4+3) = round(data.population(i,(j-1)*4+3));
        X(i,(j-1)*4+4) = data.population(i,(j-1)*4+4);
    end
    flag=zeros(1,3);
    if data.scores(i,1)<0.9
        flag(1)=0;
    end
    if data.scores(i,2)<1
        flag(2)=0;
    end
    if data.scores(i,3)<1
        flag(3)=0;
    end 
%     Y(i)=flag(1)*2^0+flag(2)*2^1+flag(3)*2^2;
    Y(i,:)=[data.scores(i,1),data.scores(i,2),data.scores(i,3)];
end
XTest = X(1:floor(0.3*m),:);
XTrain = X(floor(0.3*m)+1:end,:);
YTest = Y(1:floor(0.3*m),:);
YTrain = Y(floor(0.3*m)+1:end,:);
% [coeff,scoreTrain,~,~,explained,mu] = pca(XTrain);
% sum_explained = 0;
% idx = 0;
% explained
% while sum_explained < 95
%     idx = idx + 1;
%     sum_explained = sum_explained + explained(idx);
% end
% idx
% scoreTrain95 = scoreTrain(:,1:idx);
% mdl = fitctree(XTrain,YTrain);

%%  regression tree
% Mdl = fitrtree(XTrain,YTrain(:,1),'OptimizeHyperparameters','auto',...
%     'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName',...
%     'expected-improvement-plus'))
% resuberror = resubLoss(Mdl)
% 
% view(Mdl,'Mode','graph')

%% ensemble tree
t = templateTree('Reproducible',true);
Mdl = fitrensemble(XTrain,YTrain,'OptimizeHyperparameters','auto','Learners',t, ...
    'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName','expected-improvement-plus'))

%测试样本预测
Ynew = predict(Mdl,XTest);
%测试数据误差
train_err = YTest(:,1) - Ynew;
n1 = length(Ynew);
train_RMSE = sqrt(sum((train_err).^2)/n1);
% 执行交叉验证
partitionedModel = crossval(Mdl, 'KFold', 5);
% 计算验证预测
validationPredictions = kfoldPredict(partitionedModel);
% 计算验证 RMSE
validationRMSE = sqrt(kfoldLoss(partitionedModel, 'LossFun', 'mse'));

% scoreTest95 = (XTest-mu)*coeff(:,1:idx);

YTest_predicted = predict(Mdl,XTest);
mse(YTest_predicted,YTest)
% saveLearnerForCoder(mdl,'myMdl');

% YTest_predicted_mex = myPCAPredict(XTest,coeff(:,1:idx),mu);
% squre_sum1 = 0;
% squre_sum2 = 0;
% for i = 1:length(YTest)
%     squre_sum1 = squre_sum1 + (YTest(i)-YTest_predicted(i)).^2;
%     squre_sum2 = squre_sum2 + (YTest(i)-YTest_predicted_mex(i)).^2;
% end
% squre_sum1, squre_sum2
% isequal(YTest_predicted,YTest_predicted_mex)