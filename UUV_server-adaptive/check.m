% sco = [];
% for i = 1:500
%     sco = uuv_normal_test(population(i,:));
%     if  sco(1) ~= scores(i,1) || sco(2) ~= scores(i,2) || sco(3) ~= scores(i,3)
%         i,sco,scores(i,:)
%         sco(1)-scores(i,1), sco(2)-scores(i,2),sco(3)-scores(i,3)
% %         mse(sco,scores(i,:))
%     end
% end

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

% sco = [];
% scores = [];
% for i = 1:500
%     sco (i,:)= net(Population(i,:)'); 
%     scores (i,:)= uuv_normal_test(Population(i,:));
% end
% mse(sco,scores)
% mean(sco)
% mean(scores)

    [m,n] = size(population);
    for i = 1:m
%         for j = 1:num_incidents
%             population(i,(j-1)*4+1) = round(population(i,(j-1)*4+1));
%             population(i,(j-1)*4+2) = round(population(i,(j-1)*4+2));
%             population(i,(j-1)*4+3) = round(population(i,(j-1)*4+3));
%             population(i,(j-1)*4+4) = population(i,(j-1)*4+4);
%         end 
        Y(i,1)=scores(i,1);
        Y(i,2)=scores(i,2);
        Y(i,3)=scores(i,3);
    end
    
    X = population;
    
    
    X=X';
    Y=Y';
    hiddenLayerSize = 20;
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
    figure, plotperform(tr)
    figure, plottrainstate(tr)
    % figure, plotfit(targets,outputs)
    figure, plotregression(Y,outputs)
    figure, ploterrhist(errors)
