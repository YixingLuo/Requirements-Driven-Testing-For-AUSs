X=[];
Y=[];
data_name = 'data5.mat';
data = load(data_name);
data = data.data5;
for i = 401:1:500
    uuv = UnmannedUnderwaterVehicle();
    cond_num  = 'condition' + string(i) + '.mat';
    cond = load(cond_num);
    conditiontemp = cond.condition;
    index_name = 'index' + string(i) + '.mat';
    index = load(index_name);
    indextemp = index.index;
    for k = 1:5
        X(i-400,(k-1)*4+1) = indextemp(k);
        X(i-400,(k-1)*4+2) = conditiontemp(k,1);
        X(i-400,(k-1)*4+3) = conditiontemp(k,2);
        X(i-400,(k-1)*4+4) = conditiontemp(k,3);
    end
    flag=zeros(1,3);
    if data(i-400,1)<0.9
        flag(1)=0;
    end
    if data(i-400,3)<1
        flag(2)=0;
    end
    if data(i-400,5)<1
        flag(3)=0;
    end
        
    Y(i-400)=flag(1)*2^0+flag(2)*2^1+flag(3)*2^2;
end
XTest = X(1:70,:);
XTrain = X(71:end,:);
YTest = Y(1:70);
YTrain = Y(71:end);
[coeff,scoreTrain,~,~,explained,mu] = pca(XTrain);
sum_explained = 0;
idx = 0;
explained
while sum_explained < 95
    idx = idx + 1;
    sum_explained = sum_explained + explained(idx);
end
idx
scoreTrain95 = scoreTrain(:,1:idx);
mdl = fitctree(scoreTrain95,YTrain);
% view(mdl.Trained{1},'Mode','graph')
scoreTest95 = (XTest-mu)*coeff(:,1:idx);

YTest_predicted = predict(mdl,scoreTest95);
saveLearnerForCoder(mdl,'myMdl');

YTest_predicted_mex = myPCAPredict(XTest,coeff(:,1:idx),mu);
isequal(YTest_predicted,YTest_predicted_mex)