clc;
clear;
X=[];
Y=[];
% data_name = 'ga-multiobj-1-20201016T100507.mat';
data_name = 'ga-multiobj-10-20201018T143659.mat';
% data_name = 'ga-multiobj-5-20201016T223448.mat';
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
%     Y(i)=data.scores(i,1)*3^0+data.scores(i,2)*3^1+data.scores(i,3)*3^2;
    Y(i,1)=data.scores(i,1);
    Y(i,2)=data.scores(i,2);
    Y(i,3)=data.scores(i,3);
end
X=X';
Y=Y';

Reg1 = [X;Y(1,:)];
Reg2 = [X;Y(2,:)];
Reg3 = [X;Y(3,:)];

hiddenLayerSize = 20;
% 'trainlm'
net = fitnet(hiddenLayerSize,'trainbr');
net.divideParam.trainRatio = 70/100;
net.divideParam.valRatio = 15/100;
net.divideParam.testRatio = 15/100;
net.trainParam.epochs = 500;
net.trainParam.goal = 1e-6;

[net,tr] = train(net,X,Y);


outputs = net(X);
errors = gsubtract(outputs,Y);
performance = perform(net,Y,outputs)

save ('NN_fit_net.mat','net')

figure, plotperform(tr)
figure, plottrainstate(tr)
% figure, plotfit(targets,outputs)
figure, plotregression(Y,outputs)
figure, ploterrhist(errors)