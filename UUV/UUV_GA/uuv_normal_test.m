function f  = uuv_normal_test(x_test_initial)
global num_incidents
global goal_selection_flag
global Scores
m = num_incidents;
x_test_initial;
x_test = [];
% [m,n] = size(x_test);
for i = 1:m
    x_test(i,1) = round(x_test_initial((i-1)*4+1));
    x_test(i,2) = round(x_test_initial((i-1)*4+2));
%     if (x_test(i,2) == 5) || (x_test(i,2) == 6)
%         x_test(i,3) = 0;
%     else
        x_test(i,3) = round(x_test_initial((i-1)*4+3));
%     end
    if x_test(i,3) == 4
        x_test(i,4) = 0;
    else
        x_test(i,4) = max(0,x_test_initial((i-1)*4+4));
    end
end
x_test;
global uuv
uuv = UnmannedUnderwaterVehicle();
global pastdistance
global pasttime
global pastenergy
global pastaccuracy
global x_pre
global energy_control_pre
global dis_control_pre
global pole
x_pre = [0, 0, 0, 0, 0];
pole = 0.1;
energy_control_pre = 0;
dis_control_pre  =0;
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
planning_time = [];
current_step = 0;
need_replan = 0;


while(1)
    need_replan = 1;
%     fprintf('uuv_normal: current step %d\n', current_step);
    
    if current_step == 360
%         fprintf('last step\n');
        DS_A = min(1,pastaccuracy/uuv.acc_target);
        DS_D = min(1,pastdistance/uuv.distance_target);
        if pastenergy <=  uuv.energy_target
            DS_E = 1;
        else
            DS_E = (uuv.energy_budget - pastenergy)/(uuv.energy_budget - uuv.energy_target);
        end
%         DS_E = min(1,(1-(pastenergy - uuv.energy_target)/(uuv.energy_budget-uuv.energy_target)));
        data = [DS_A, pastaccuracy, DS_D, pastdistance, DS_E, pastenergy];

%         f = [];
%         if goal_selection_flag(1) == 0 %% maximize this goal
%             f = [f, -pastaccuracy];
%         else %% minimize this goal
%             f = [f, pastaccuracy];
%         end
%         if goal_selection_flag(2) == 0 %% maximize this goal
%             f = [f, -pastdistance];
%         else %% minimize this goal
%             f = [f, pastdistance];
%         end
%         if goal_selection_flag(3) == 0 %% minimize this goal
%             f = [f, pastenergy];
%         else %% maximize this goal
%             f = [f, -pastenergy];
%         end
%         f = [goal_selection_flag(1)*pastaccuracy, goal_selection_flag(2)*pastdistance, -goal_selection_flag(3)*pastenergy];
        Scores = [Scores; abs(pastaccuracy),  abs(pastdistance), abs(pastenergy)];
%         f = DS_A + DS_D + DS_E;
%         f = [DS_A, DS_D, DS_E];
        f = [pastaccuracy,pastdistance, - 0.5*pastenergy];
        break
    end

  
    for i = 1:m
        if current_step == x_test(i,1)
            need_replan = 1;
            index_cond = i;
                if x_test(index_cond,2) == 1
                    uuv = SensorError(uuv, x_test(index_cond,3), x_test(index_cond,4));  
                elseif x_test(index_cond,2) == 2
                    uuv = EnergyDisturbance(uuv, x_test(index_cond,3), x_test(index_cond,4));
                    elseif x_test(index_cond,2) == 3
                         uuv = SpeedDisturbance(uuv, x_test(index_cond,3), x_test(index_cond,4));
                        elseif x_test(index_cond,2) == 4
                            uuv = SensorFailure(uuv, x_test(index_cond,3));    
                            elseif x_test(index_cond,2) == 5
                                uuv = EnergyBudget(uuv, x_test(index_cond,4));
                                    elseif x_test(index_cond,2) == 6
                                        uuv = DistanceBudget(uuv, x_test(index_cond,4));
                end
            break
        end
    end
    
    
    
    if current_step == 1
        need_replan = 1;
    end
    exitflag = 0;
    if need_replan == 1 
        t1=clock;
        for iternum = 1:1:1
            lb=[];
            ub=[];
            x0=[];
            for i = 1 : uuv.N_s % portion of time
                lb(i) = 0;
                ub(i) = 1;
                x0(i) = 0.2;
            end
            options.Algorithm = 'sqp'; 
            options.Display = 'off';
            tic;
            [x,fval,exitflag]=fmincon(@objuuv_normal,x0,[],[],[],[],lb,ub,@myconuuv_normal,options);
            t2 = toc;
            if exitflag > 0 
%                 fprintf(2,'uuv_normal: have solution at current step: %d , %d\n',exitflag, current_step);
                fval_pre = fval;
%                 x_pre = x;            
                break
            end     
        end
        planning_time = [planning_time; t2];
        
%         if exitflag < 0
%             for iternum = 1:1:20
%                 lb=[];
%                 ub=[];
%                 x0=[];
%                 for i = 1 : uuv.N_s % portion of time
%                     lb(i) = 0;
%                     ub(i) = 1;
%                     x0(i) = unifrnd(0,1);
%                 end
%                 options.Algorithm = 'sqp'; 
%                 options.Display = 'off';
%                 tic;
%                 [x,fval,exitflag]=fmincon(@objuuv_relax,x0,[],[],[],[],lb,ub,@myconuuv_relax,options);
%                 t2 = toc;
%                 if exitflag > 0 
%                     fprintf(2,'uuv_relax: have solution at current step: %d , %d\n',exitflag, current_step);
%                     fval_pre = fval;
%                     x_pre = x;            
%                     break
%                 end     
%             end
%         end

        %% distance
        time_left = uuv.time_target - pasttime;
        
        dis_pre = 0;
        for i = 1:uuv.N_s
            if uuv.s_work(i) == 1
                dis_pre = dis_pre + x_pre(i)*uuv.s_speed(i);
            end
        end
        dis_control_pre = dis_control_pre + pole*((uuv.distance_target-pastdistance)/(time_left) - dis_pre);
        
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
        engy_pre = 0;
        for i = 1:uuv.N_s
            if uuv.s_work(i) == 1
                engy_pre = engy_pre + x_pre(i)*uuv.s_energy(i);
            end
        end
        
        energy_control_pre = energy_control_pre + pole*((uuv.energy_target-pastenergy)/(uuv.time_target - pasttime) - engy_pre);
        
        engy = 0;
        for i = 1:uuv.N_s
           if uuv.s_work(i) == 1
            engy = engy + x(i)*uuv.s_energy(i);     
           end
        end
        pastenergy = pastenergy + engy * uuv.time_step;
        energy_list = [energy_list, engy];             
 
        
        %% sensor usage
        index = 1;
        for i = 1:length(uuv.s_work)
            if uuv.s_work(i) == 1                  
                usage_plan(current_step+1, i) = x(index);
                index = index+1;
            else
                usage_plan(current_step+1, i) = 0;
            end
        end
        
   	  %% time
        pasttime = pasttime + uuv.time_step;  
        
        x_pre = x;
        
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
                usage_plan(current_step+1, i) = x_pre(index);
                index = index+1;
            else
                usage_plan(current_step+1, i) = 0;
            end
        end       
    end
    current_step = current_step + 1;

    end
end
