function Population = initialize_variables(GenomeLength, uuv_normal_test, options)
Population = [];
totalpopulation = sum(options.PopulationSize);
global num_incidents
global uuv
global initial_ratio
global best_pop
global start_generation
global goal_selection_flag
global priority_list
if start_generation == 1
    initial_ratio = 1;
else
    initial_ratio = 0.5;
end
for pop = 1:1:totalpopulation*initial_ratio
    uuv = UnmannedUnderwaterVehicle();
    l = 1:1:15;
    disturb = randi([1,4],1,l(num_incidents));
    a=2:359;
    K=randperm(length(a));
    N=length(disturb);
    index1 = a(K(1:N));
    % index1 = randperm(359,length(disturb));
    index = sort(index1);
    condition = [];
    failure_list = [];
    for i = 1: length(disturb)
        if disturb(i) == 1
            idx = unidrnd(5);   
            acc_ratio = 40*rand;
    %             acc = uuv.s_accuracy(idx)*acc_ratio/100;
            condition(i,:) = [1,idx,acc_ratio];
        elseif disturb(i) == 2
            idx = unidrnd(5);
            energy_ratio = 40*rand;
    %             energy = uuv.s_energy(idx)*energy_ratio/100;
            condition(i,:) = [2,idx,energy_ratio];
       elseif disturb(i) == 3
            idx = unidrnd(5);
            speed_ratio = 40*rand;
    %             speed = uuv.s_speed(idx)*speed_ratio/100;
            condition(i,:) = [3,idx,speed_ratio];   
        elseif disturb(i) == 4
            idx = unidrnd(5);
            if any (idx == failure_list)
                idx = unidrnd(5);
            end
            condition(i,:) = [4,idx,0];
        elseif disturb(i) == 5 
            idx = unidrnd(5);
            energy_target_ratio = 20*rand;
            condition(i,:) = [5,0,energy_target_ratio]; 
        elseif disturb(i) == 6
            idx = unidrnd(5);
            dis_target_ratio = 20*rand;
            condition(i,:) = [6,0,dis_target_ratio]; 
        end
    end
    x_test_initial = [];
    for i = 1: length(disturb)
    %         x0(i,1) = index (i);
    %         x0(i,2) = condition(i,1);
    %         x0(i,3) = condition(i,2);
    %         x0(i,4) = condition(i,3);
        x_test_initial((i-1)*4+1) = index (i);
        x_test_initial((i-1)*4+2) = condition(i,1);
        x_test_initial((i-1)*4+3) = condition(i,2);
        x_test_initial((i-1)*4+4) = condition(i,3);
    end
    %     f  = uuv_normal_test(x_test_initial);
    Population(pop,1:4*num_incidents) =  x_test_initial;
    %     for fit = 1:1:3
    %         Population(pop,fit+4*num_incidents)=f(fit);
    %     end
end
if start_generation > 1
    for i = 1:size(priority_list,1)
        if priority_list(i,:)==goal_selection_flag
            index = i;
        end
    end
    Population(totalpopulation*initial_ratio + 1: totalpopulation,:) = best_pop (1:totalpopulation*initial_ratio,:,index);
end
end

