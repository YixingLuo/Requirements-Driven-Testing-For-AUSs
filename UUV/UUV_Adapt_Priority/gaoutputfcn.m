function [state,options,optchanged] = gaoutputfcn(options,state,flag)
global datafolder
global start_generation
global goal_selection_flag
global goal_scores
global goal_round
global priority_list
global scenario_pop
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
    fitness = [];
    result = [];
    [m,n] = size(state.Population);
    for i = 1:m
        for j = 1:floor(n/4)
            Pop(i,(j-1)*4+1) = round(state.Population(i,(j-1)*4+1));
            Pop(i,(j-1)*4+2) = round(state.Population(i,(j-1)*4+2));
            Pop(i,(j-1)*4+3) = round(state.Population(i,(j-1)*4+3));
            if Pop(i,(j-1)*4+3) == 3
                Pop(i,(j-1)*4+4) = 0;
            else
                Pop(i,(j-1)*4+4) =  max(0, state.Population(i,(j-1)*4+4));
            end
        end
        for fun_num = 1:size(state.Score,2)
            fitness(i,fun_num) = state.Score(i,fun_num);
        end
        for j = 1:size(scenario_pop,1)
            if scenario_pop(j,:) == Pop(i,:)
                result = [result; goal_scores(j,:)];
                break
            end
        end
%         fitness(i,1)=state.Score(i,1);
%         fitness(i,2)=state.Score(i,2);
%         fitness(i,3)=state.Score(i,3);
    end
%     datafolder, start_generation
    name =  'interval-results-'+ string(start_generation)+ '.mat';
    path = strcat(datafolder,'/',name);
    save(path,'Pop', 'fitness','goal_selection_flag', 'goal_scores','result','scenario_pop');
    
    result = [];
    count = zeros(1,8);
    count_list = [];
    for k = 1:1000
        name = 'interval-results-' + string(k) + '.mat';
        filename = strcat(datafolder,'/',name);
        if exist(filename,'file')==0
            count_list = [count_list; count];
            break
        end
        data = load(filename);
        data1 = data.fitness;
        [m,n] = size(data1);
    
        for i = 1:1:m
            temp_result = data1(m,:);
            goal_flag = zeros(1,3);
            if abs(temp_result(1))< 0.9
                goal_flag(1) = 1;
            end
            if abs(temp_result(2))< 100*1000
                goal_flag(2) = 1;
            end
            if abs(temp_result(3))> 5.4*1e6
                goal_flag(3) = 1;
            end
            sum = goal_flag(1)*2^0 + goal_flag(2)*2^1 + goal_flag(3)*2^2 + 1;
            for j = 1:size(priority_list,1)
                if priority_list(j,:) == goal_flag
                    count(j) = count(j) + 1;
                    break
                end
            end
        end
    end
    if mod (start_generation,goal_round)==0 
        start = 1;
        for i = 1:size(priority_list,1)
            if count(i) == 0
                start = i;
                break;
            end
        end
    goal_selection_flag = priority_list(start,:);        
    end
    
    goal_scores = [];
    scenario_pop = [];
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