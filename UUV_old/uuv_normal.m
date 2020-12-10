function [data,usage_plan,planning_time] = uuv_normal(nnum, indextemp)
global uuv
uuv = UnmannedUnderwaterVehicle();
global pastdistance
global pasttime
global pastenergy
global pastaccuracy
pastdistance = 0;
pasttime = 0;
pastenergy = 0;
pastaccuracy = 0;
usage_plan = [];
x_plan_relax=[];
x_plan = [];
speed = [];
acc_list = [];
distance_list = [];
energy_list = [];
flag = [];
f_value = [];
flag_relax = [];
f_value_relax = [];
log = [];
results =[];
x_pre = [];
planning_time = [];
current_step = 1;
% name = 'condition' + string(946) + '.mat';
name = 'condition' + string(nnum) + '.mat';
cond = load(name);
need_replan = 0;
% name = 'index' + string(946) + '.mat';
% index = load(name);
% indextemp = index.index;
plan_num = length(indextemp);
index_cond = 1;

while(1)
    need_replan = 0;
%     fprintf('uuv_normal: current step %d\n', current_step);
    
    if current_step > 360
        fprintf('last step\n');
        DS_A = min(1,pastaccuracy);
        DS_D = min(1,pastdistance/uuv.distance_target);
        DS_E = min(1,(1-(pastenergy - uuv.energy_target)/(uuv.energy_budget-uuv.energy_target)));
        data = [DS_A, pastaccuracy, DS_D, pastdistance, DS_E, pastenergy];
        break
    end
    
    if  plan_num > 0 && current_step == indextemp(index_cond)        
        need_replan = 1;
        plan_num = plan_num - 1;      
        if cond.condition(index_cond,1) == 1
            uuv = SensorError(uuv, cond.condition(index_cond,2), cond.condition(index_cond,3));  
        elseif cond.condition(index_cond,1) == 2
            uuv = EnergyDisturbance(uuv, cond.condition(index_cond,2), cond.condition(index_cond,3));
            elseif cond.condition(index_cond,1) == 3
                 uuv = SpeedDisturbance(uuv, cond.condition(index_cond,2), cond.condition(index_cond,3));
                elseif cond.condition(index_cond,1) == 4
                    uuv = SensorFailure(uuv, cond.condition(index_cond,2));    
        end
        index_cond = index_cond+1;
    end
    
    if current_step == 1
        need_replan = 1;
    end
    exitflag = 0;
    if need_replan == 1 
        t1=clock;
        for iternum = 1:1:20
            lb=[];
            ub=[];
            x0=[];
            for i = 1 : uuv.N_s % portion of time
                lb(i) = 0;
                ub(i) = 1;
                x0(i) = unifrnd(0,1);
            end
            options.Algorithm = 'sqp'; 
            options.Display = 'off';
            tic;
            [x,fval,exitflag]=fmincon(@objuuv_normal,x0,[],[],[],[],lb,ub,@myconuuv_normal,options);
            t2 = toc;
            if exitflag > 0 
                fprintf(2,'uuv_normal: have solution at current step: %d , %d\n',exitflag, current_step);
                fval_pre = fval;
                x_pre = x;            
                break
            end     
        end
        planning_time = [planning_time; t2];
        
        if exitflag < 0
            for iternum = 1:1:20
                lb=[];
                ub=[];
                x0=[];
                for i = 1 : uuv.N_s % portion of time
                    lb(i) = 0;
                    ub(i) = 1;
                    x0(i) = unifrnd(0,1);
                end
                options.Algorithm = 'sqp'; 
                options.Display = 'off';
                tic;
                [x,fval,exitflag]=fmincon(@objuuv_relax,x0,[],[],[],[],lb,ub,@myconuuv_relax,options);
                t2 = toc;
                if exitflag > 0 
                    fprintf(2,'uuv_relax: have solution at current step: %d , %d\n',exitflag, current_step);
                    fval_pre = fval;
                    x_pre = x;            
                    break
                end     
            end
        end

        %% distance
        speed_now = 0;
        for i = 1:uuv.N_s
            if uuv.s_work(i) == 1
                speed_now = speed_now + x(i)*uuv.s_speed(i);
            end
        end
        speed = [speed, speed_now];
        pastdistance = pastdistance + speed_now * uuv.time_step;
        distance_list = [distance_list, pastdistance];
        
       %% accuracy
        acc = 0;
        for i = 1:uuv.N_s
            if uuv.s_work(i) == 1
                acc = acc + x(i)*uuv.s_accuracy(i);
            end
        end
        acc_list = [acc_list, acc];
        pastaccuracy = (pastaccuracy * pasttime + acc * uuv.time_step) / (pasttime + uuv.time_step);
         
        %% energy
        engy = 0;
        for i = 1:uuv.N_s
           if uuv.s_work(i) == 1
            engy = engy + x(i)*uuv.s_energy(i);     
           end
        end
        pastenergy = pastenergy + engy * uuv.time_step;
        energy_list = [energy_list, engy];       
    
        %% time
        pasttime = pasttime + uuv.time_step;   
        
        %% sensor usage
        index = 1;
        for i = 1:length(uuv.s_work)
            if uuv.s_work(i) == 1                  
                usage_plan(current_step, i) = x(index);
                index = index+1;
            else
                usage_plan(current_step, i) = 0;
            end
        end
    else
        %% distance
        speed_now = 0;
        for i = 1:uuv.N_s
            if uuv.s_work(i) == 1
%                 uuv.s_work, x_pre
                speed_now = speed_now + x_pre(i)*uuv.s_speed(i);
            end
        end
        speed = [speed, speed_now];
        pastdistance = pastdistance + speed_now * uuv.time_step;
        distance_list = [distance_list, pastdistance];
        
       %% accuracy
        acc = 0;
        for i = 1:uuv.N_s
            if uuv.s_work(i) == 1
                acc = acc + x_pre(i)*uuv.s_accuracy(i);
            end
        end
        acc_list = [acc_list, acc];
        pastaccuracy = (pastaccuracy * pasttime + acc * uuv.time_step) / (pasttime + uuv.time_step);
         
        %% energy
        engy = 0;
        for i = 1:uuv.N_s
            if uuv.s_work(i) == 1
                engy = engy + x_pre(i)*uuv.s_energy(i);
            end
        end
        pastenergy = pastenergy + engy * uuv.time_step;
        energy_list = [energy_list, engy];       
    
        %% time
        pasttime = pasttime + uuv.time_step;   
        
        %% sensor usage
        index = 1;
        for i = 1:length(uuv.s_work)
            if uuv.s_work(i) == 1                  
                usage_plan(current_step, i) = x_pre(index);
                index = index+1;
            else
                usage_plan(current_step, i) = 0;
            end
        end       
    end
    current_step = current_step + 1;

    end
end