clc;
clear;
X=[];
Y=[];
% data_name = 'ga-multiobj-1-20201016T100507.mat';
% data_name = 'ga-multiobj-10-20201018T143659.mat';
data_name = 'ga-multiobj-5-20201016T223448.mat';
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
    Y(i)=data.scores(i,1)*3^0+data.scores(i,2)*3^1+data.scores(i,3)*3^2;
end
XTest = X(1:floor(0.3*m),:);
XTrain = X(floor(0.3*m)+1:end,:);
YTest = Y(1:floor(0.3*m));
YTrain = Y(floor(0.3*m)+1:end);
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
squre_sum1 = 0;
squre_sum2 = 0;
for i = 1:length(YTest)
    squre_sum1 = squre_sum1 + (YTest(i)-YTest_predicted(i)).^2;
    squre_sum2 = squre_sum2 + (YTest(i)-YTest_predicted_mex(i)).^2;
end
squre_sum1, squre_sum2
% isequal(YTest_predicted,YTest_predicted_mex)