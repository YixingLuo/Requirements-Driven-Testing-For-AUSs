function [x,fval,exitflag,output,population,score] = option(MaxGenerations_Data,MaxTime_Data,FunctionTolerance_Data,ConstraintTolerance_Data,InitialPopulationMatrix_Data)
%% This is an auto generated MATLAB file from Optimization Tool.

%% Start with the default options
options = optimoptions('gamultiobj');
%% Modify options setting
options = optimoptions(options,'MigrationDirection', 'both');
options = optimoptions(options,'MaxGenerations', MaxGenerations_Data);
options = optimoptions(options,'MaxTime', MaxTime_Data);
options = optimoptions(options,'FunctionTolerance', FunctionTolerance_Data);
options = optimoptions(options,'ConstraintTolerance', ConstraintTolerance_Data);
options = optimoptions(options,'InitialPopulationMatrix', InitialPopulationMatrix_Data);
options = optimoptions(options,'CreationFcn', @randomsituation_test);
options = optimoptions(options,'CrossoverFcn', {  @crossoverintermediate [] });
options = optimoptions(options,'MutationFcn', @mutationadaptfeasible);
options = optimoptions(options,'Display', 'final');
options = optimoptions(options,'PlotFcn', {  @gaplotscorediversity @gaplotpareto @gaplotparetodistance @gaplotspread });
[x,fval,exitflag,output,population,score] = ...
gamultiobj([],[],[],[],[],[],[],[],[],options);
