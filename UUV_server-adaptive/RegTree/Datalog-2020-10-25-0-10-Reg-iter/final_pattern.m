Population = [];
Scores = [];
for model_index = 1:10
    name = 'ga-multiobj-adaptive-iter-10-'+ string(model_index) + '.mat';
    pre_result = load(name);
    Population = [Population;pre_result.population];
    Scores = [Scores; pre_result.scores];
end
[m,n] = size(Population);
for i = 1:m
    for j = 1:num_incidents
        Population(i,(j-1)*4+1) = round(Population(i,(j-1)*4+1));
        Population(i,(j-1)*4+2) = round(Population(i,(j-1)*4+2));
        Population(i,(j-1)*4+3) = round(Population(i,(j-1)*4+3));
        Population(i,(j-1)*4+4) = Population(i,(j-1)*4+4);
    end   
    Y(i,1)=Scores(i,1);
    Y(i,2)=Scores(i,2);
    Y(i,3)=Scores(i,3);
end
    
    X = Population;

for i = 1:3
    Mdl = fitrtree(X,Y(:,i),'OptimizeHyperparameters','auto',...
    'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName',...
    'expected-improvement-plus'));
    model_name = 'Reg_model-'+ string(iter) + '-final-'+ string(i);
    model_name = strcat(model_name);
    save (model_name,'Mdl');
end
