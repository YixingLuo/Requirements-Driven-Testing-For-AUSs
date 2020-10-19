clc;
clear;
X=[];
Y=[];
data_name = 'ga-multiobj-1-20201016T100507.mat';
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
    Y(i)=data.scores(i,1)*2^0+data.scores(i,2)*2^1+data.scores(i,3)*2^2;
end
XTest = X(1:floor(0.7*m),:);
XTrain = X(floor(0.7*m)+1:end,:);
YTest = Y(1:floor(0.7*m));
YTrain = Y(floor(0.7*m)+1:end);
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
mdl = fitctree(scoreTrain95,YTrain,'CrossVal','on');
view(mdl.Trained{1},'Mode','graph')
scoreTest95 = (XTest-mu)*coeff(:,1:idx);

YTest_predicted = predict(mdl,scoreTest95);
saveLearnerForCoder(mdl,'myMdl');

YTest_predicted_mex = myPCAPredict(XTest,coeff(:,1:idx),mu);
isequal(YTest_predicted,YTest_predicted_mex)