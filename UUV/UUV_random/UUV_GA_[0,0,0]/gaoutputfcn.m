function [state,options,optchanged] = gaoutputfcn(options,state,flag)
global datafolder
global start_generation
%GAOUTPUTFCNTEMPLATE Template to write custom OutputFcn for GA or GAMULTIOBJ.
%   [STATE, OPTIONS, OPTCHANGED] = GAOUTPUTFCNTEMPLATE(OPTIONS,STATE,FLAG)
%
%   STATE: A structure containing the following information about the state 
%   of the optimization for GA:
%             Generation: Current generation number
%              StartTime: Time when GA started, returned by TIC
%               StopFlag: Character vector containing the reason for stopping
%        LastImprovement: Generation at which the last improvement in
%                         fitness value occurred
%    LastImprovementTime: Time at which last improvement occurred
%                   Best: Vector containing the best score in each generation
%                    how: String describing the 'auglag' nonlinear
%                         constraint step
%                FunEval: Cumulative number of function evaluations
%            Expectation: Expectation for selection of individuals
%              Selection: Indices of individuals selected for elite,
%                         crossover and mutation
%             Population: Population in the current generation
%                  Score: Scores of the current population
%             NonLinIneq: Nonlinear inequality constraint violations,
%                         exists for noninteger problems with nonlinear constraints
%              NonLineEq: Nonlinear equality constraint violations,
%                         exists for noninteger problems with nonlinear constraints
%       LinearConstrType: Type of linear constraints, one of 'boundconstraints',
%                         'linearconstraints', or 'unconstrained'
%         IsMixedInteger: Boolean value, true for integer-constrained problems
%
%
%   STATE for GAMULTIOBJ:
%             Generation: Current generation number
%              StartTime: Time when GA started, returned by TIC
%               StopFlag: Character vector containing the reason for stopping
%                FunEval: Cumulative number of function evaluations
%              Selection: Indices of individuals selected for elite,
%                         crossover and mutation
%                  mIneq: Number of nonlinear inequality constraints
%                    mEq: Number of nonlinear equality constraints
%                   mAll: Number of nonlinear constraints = mIneq + mEq
%             Population: Population in the current generation
%                      C: Nonlinear inequality constraints at current point
%                    Ceq: Nonlinear equality constraints at current point
%                 isFeas: Feasibility of population, a logical vector
%           maxLinInfeas: Maximum infeasibility with respect to linear constraints
%                  Score: Scores of the current population
%                   Rank: Vector of ranks of population
%               Distance: Vector of distances of each member of the population
%                         to the nearest neighboring member
%        AverageDistance: Average of Distance
%                 Spread: Vector of spread in each generation
%       LinearConstrType: Type of linear constraints, one of 'boundconstraints',
%                         'linearconstraints', or 'unconstrained'
%         IsMixedInteger: false (gamultiobj does not support integer constraints)
%
%   FLAG: Current state in which OutputFcn is called. Possible values are:
%         init: initialization state 
%         iter: iteration state
%    interrupt: subproblem for nonlinear constraints state
%         done: final state
%
%   OPTIONS: Options object as created by OPTIMOPTIONS.
% 		
%   OPTCHANGED: Boolean indicating if the options have changed. Set to true
%   to have new the solver use new options.
%
%   Stop the solver by setting STATE.StopFlag to a nonempty value such as
%   'Y'.
%
%	See also GA, GAMULTIOBJ

%   Copyright 2004-2016 The MathWorks, Inc.

% disp(state.FunEval)
optchanged = false;

if state.isFeas
    Pop = [];
    scores = [];
    [m,n] = size(state.Population);
    for i = 1:m
        for j = 1:floor(n/4)
            Pop(i,(j-1)*4+1) = round(state.Population(i,(j-1)*4+1));
            Pop(i,(j-1)*4+2) = round(state.Population(i,(j-1)*4+2));
            Pop(i,(j-1)*4+3) = round(state.Population(i,(j-1)*4+3));
            Pop(i,(j-1)*4+4) = state.Population(i,(j-1)*4+4);
        end
        scores(i,1)=state.Score(i,1);
        scores(i,2)=state.Score(i,2);
        scores(i,3)=state.Score(i,3);
    end
    name =  'interval-results-'+ string(start_generation)+ '.mat';
    path = strcat(datafolder,'/',name);
    save(path,'Pop', 'scores');
    start_generation = start_generation + 1;
end

switch flag
    case 'init'
        disp('Starting the algorithm');
    case {'iter','interrupt'}
        disp('Iterating ...')
    case 'done'
        disp('Performing final task');
end