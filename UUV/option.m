function [x,fval,exitflag,output,population,score] = option(PopulationSize_Data,MaxGenerations_Data,MaxTime_Data)
%% This is an auto generated MATLAB file from Optimization Tool.

%% Start with the default options
options = optimoptions('gamultiobj');
%% Modify options setting
options = optimoptions(options,'PopulationSize', PopulationSize_Data);
options = optimoptions(options,'MigrationDirection', 'both');
options = optimoptions(options,'MaxGenerations', MaxGenerations_Data);
options = optimoptions(options,'MaxTime', MaxTime_Data);
options = optimoptions(options,'CrossoverFcn', {  @crossoverintermediate [] });
options = optimoptions(options,'MutationFcn', @mutationadaptfeasible);
options = optimoptions(options,'Display', 'final');
options = optimoptions(options,'PlotFcn', {  @gaplotdistance @gaplotscorediversity @gaplotpareto @gaplotspread });
[x,fval,exitflag,output,population,score] = ...
gamultiobj([],[],[],[],[],[],[],[],[],options);
