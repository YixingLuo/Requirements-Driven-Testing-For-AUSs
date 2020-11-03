%% statics for soft goal violaiton
count = [];
i1=[];
i2=[];
d1=[];
d2=[];
condition = [];
condition2 = [];
for i = 1:size(data1,1)
    if (data2(i,3)>0&&data2(i,3)<=(1-1e-4))||(data2(i,5)>0&&data2(i,5)<=(1-1e-4))
        count = [count,i];
        i1 = [i1;index(i,:)];
        i2 = [i2;index2(i,:)];
        d1 = [d1;data1(i,:)];
        d2 = [d2;data2(i,:)];
    end
end

for i = 1:length(count)
    name = 'condition' + string(count(i));
    cond = load(name);
    temp_cond = [];
    for j = 1:size(i1,2)
        temp_cond = [temp_cond; [i1(i,j),cond.condition(j,:)]];
    end
    condition = [condition; temp_cond];
    temp_cond = [];
    for j = 1:size(i2,2)
        temp_cond = [temp_cond; [i2(i,j),cond.condition(j,:)]];
    end
    condition2 = [condition2; temp_cond];
end

%% establish regression tree
% datafolder = 'soft-goal-violation';
% datalog_name = strcat(datafolder,'/data20201103T215532','.mat');
% datalog = load(datalog_name);
% num = 1;
% for i = 1:1000
%     name = strcat(datafolder,'/condition', string(i),'.mat');
%     name_idx = strcat(datafolder,'/index', string(i),'.mat');
%     if exist(name)
%         cond = load(name);
%         index = load(name_idx);
%         for j = 1:size(cond.condition,1)
%             X(num,(j-1)*4+1) = index.indextemp(j);
%             X(num,(j-1)*4+2) = cond.condition(j,1);
%             X(num,(j-1)*4+3) = cond.condition(j,2);
%             X(num,(j-1)*4+4) = cond.condition(j,3);
%         end
%         Y(num,:) = [datalog.data1(i,1), datalog.data1(i,3), datalog.data1(i,5)];
%         num = num + 1;      
%     end
% end
% 
% for i = 1:3
%     Mdl = fitrtree(X,Y(:,i),'OptimizeHyperparameters','auto',...
%     'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName',...
%     'expected-improvement-plus'));
%     model_name = 'Reg_model-'+ string(i);
%     model_name = strcat(datafolder,'/',model_name);
%     save (model_name,'Mdl')
% end


